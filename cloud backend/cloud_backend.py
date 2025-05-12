from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    print("Received JSON:", data)

    code = data.get("code")
    arch = data.get("architecture")

    if not code or not arch:
        return jsonify({"error": "Missing code or architecture"}), 400

    try:
        if arch == "x86":
            return run_x86(code)
        elif arch == "mips32":
            return run_mips(code)
        elif arch == "arm":
            return run_arm(code)
        else:
            return jsonify({"error": "Unsupported architecture"}), 400
    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": f"Assembly failed with return code {e.returncode}",
            "output": e.output.decode()
        }), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_x86(code):
    with tempfile.TemporaryDirectory() as tmpdir:
        asm_file = os.path.join(tmpdir, "program.asm")
        obj_file = os.path.join(tmpdir, "program.o")
        bin_file = os.path.join(tmpdir, "program")

        with open(asm_file, "w") as f:
            f.write(code)

        # Assemble
        subprocess.run(["nasm", "-felf32", asm_file, "-o", obj_file], check=True)
        # Link
        subprocess.run(["ld", "-m", "elf_i386", obj_file, "-o", bin_file], check=True)
        # Execute
        output = subprocess.check_output([bin_file], stderr=subprocess.STDOUT).decode()
        return jsonify({"output": output})

def run_mips(code):
    with tempfile.TemporaryDirectory() as tmpdir:
        asm_path = os.path.join(tmpdir, "program.asm")
        with open(asm_path, "w") as f:
            f.write(code)

        result = subprocess.run(
            ["spim",'-q',"-file", asm_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False  # spim often returns non-zero even on success
        )

        if result.stderr and "exception" in result.stderr.lower():
            return jsonify({
                "error": "MIPS execution error",
                "output": result.stderr
            }), 400

        return jsonify({"output": result.stdout})

def run_arm(code):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            asm_path = os.path.join(tmpdir, "program.s")
            obj_path = os.path.join(tmpdir, "program.o")
            bin_path = os.path.join(tmpdir, "program")

            with open(asm_path, "w") as f:
                f.write(code.strip() + "\n")

            # Assemble
            result = subprocess.run([
                "arm-linux-gnueabi-as",
                asm_path,
                "-o", obj_path
            ], stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                return jsonify({"error": "Assembly failed", "details": result.stderr}), 400

            # Link
            result = subprocess.run([
                "arm-linux-gnueabi-ld",
                obj_path,
                "-o", bin_path
            ], stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                return jsonify({"error": "Linking failed", "details": result.stderr}), 400

            # Run
            output = subprocess.check_output([
                "qemu-arm", "-L", "/usr/arm-linux-gnueabi/", bin_path
            ], stderr=subprocess.STDOUT).decode()

            return jsonify({"output": output})

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Execution failed",
            "details": e.output.decode() if e.output else "No output"
        }), 400
    except Exception as e:
        return jsonify({"error": "Unknown error", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)