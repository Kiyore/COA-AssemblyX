from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

# Dummy user credentials
users = {
    'test': '123'
}

# Sample questions dictionary
questions = {
  'x86_hello': {
    'title': 'Say Hello World to Assembly',
    'description': 'Write a program in x86 Assembly to print "Hello, World!"',
    'boilerplate': 'section .text\n    global _start\n\n_start:\n    ; Your x86 code here\n    mov eax, 1\n    mov ebx, 0\n    int 0x80',
    'expectedOutput': 'Hello, World!\n'
  },
  'add': {
    'title': 'Basic Addition in Assembly',
    'description': 'Write a program to add 5 and 3',
    'boilerplate': 'section .text\n    global _start\n\n_start:\n    ; Your x86 code here\n    mov eax, 1\n    mov ebx, 0\n    int 0x80',
    'expectedOutput': '8\n'
  },
  'sub': {
    'title': 'Basic Subtraction in Assembly',
    'description': 'Write a program to subtract 2 from 5',
    'boilerplate': 'section .text\n    global _start\n\n_start:\n    ; Your x86 code here\n    mov eax, 1\n    mov ebx, 0\n    int 0x80',
    'expectedOutput': '3\n'
  },
  'mul': {
    'title': 'Basic Multiplication in Assembly',
    'description': 'Write a program to multiply 3 and 3',
    'boilerplate': 'section .text\n    global _start\n\n_start:\n    ; Your x86 code here\n    mov eax, 1\n    mov ebx, 0\n    int 0x80',
    'expectedOutput': '9\n'
  },
  'div': {
    'title': 'Basic Division in Assembly',
    'description': 'Write a program to divide 10 by 2',
    'boilerplate': 'section .text\n    global _start\n\n_start:\n    ; Your x86 code here\n    mov eax, 1\n    mov ebx, 0\n    int 0x80',
    'expectedOutput': '5\n'
  }
}

solutions = {
    'x86_hello': {
       'x86': 'section .data\n    msg db \'Hello, World!\', 0xA\n    len equ $ - msg\n\nsection .text\n    global _start\n\n_start:\n    mov eax, 4\n    mov ebx, 1\n    mov ecx, msg\n    mov edx, len\n    int 0x80\n\n    mov eax, 1\n    xor ebx, ebx\n    int 0x80',
        'mips': '.data\n    msg: .asciiz "Hello, World!\\n"\n\n.text\n    .globl main\n\nmain:\n    li $v0, 4\n    la $a0, msg\n    syscall\n\n    li $v0, 10\n    syscall',
        'arm': '.data\n    msg: .asciz "Hello, World!\\n"\n\n.text\n    .global _start\n\n_start:\n    mov r7, #4\n    mov r0, #1\n    ldr r1, =msg\n    mov r2, #14\n    svc #0\n\n    mov r7, #1\n    mov r0, #0\n    svc #0'
    },
    'add': {
      'x86': 'section .data\n    result db 0\n\nsection .text\n    global _start\n\n_start:\n    mov eax, 3\n    mov ebx, 5\n    add eax, ebx\n    add al, \'0\'\n    mov [result], al\n    mov eax, 4\n    mov ebx, 1\n    mov ecx, result\n    mov edx, 1\n    int 0x80\n    mov eax, 1\n    xor ebx, ebx\n    int 0x80',
      'mips': '.data\nresult: .byte 0\n\n.text\n.globl main\n\nmain:\n    li $t0, 3\n    li $t1, 4\n    add $t2, $t0, $t1\n    addi $t2, $t2, 48\n    la $a0, result\n    sb $t2, 0($a0)\n\n    li $v0, 4\n    la $a0, result\n    syscall\n\n    li $v0, 10\n    syscall',
      'arm': '.section .text\n.global _start\n_start:\n    mov r0, #5\n    mov r1, #3\n    add r2, r0, r1\n    add r2, r2, #\'0\'\n    ldr r1, =result\n    strb r2, [r1]\n    mov r0, #1\n    ldr r1, =result\n    mov r2, #1\n    mov r7, #4\n    svc #0\n    mov r7, #1\n    mov r0, #0\n    svc #0\n.section .data\nresult:\n    .byte 0'
    },
    'sub': {
        'x86': 'section .data\n    result db 0\n\nsection .text\n    global _start\n\n_start:\n    mov eax, 5\n    sub eax, 2\n    add al, \'0\'\n    mov [result], al\n\n    mov eax, 4\n    mov ebx, 1\n    mov ecx, result\n    mov edx, 1\n    int 0x80\n\n    mov eax, 1\n    xor ebx, ebx\n    int 0x80',
        'mips': '.data\n    result: .asciiz "0\\n"\n\n.text\n.globl main\n\nmain:\n    li $t0, 5\n    li $t1, 3\n    sub $t2, $t0, $t1\n\n    addi $t2, $t2, 48\n    sb $t2, result\n\n    li $v0, 4\n    la $a0, result\n    syscall\n\n    li $v0, 10\n    syscall',
        'arm': '.section .data\nresult:\n    .byte 0\n\n.section .text\n.global _start\n\n_start:\n    mov r0, #5\n    mov r1, #3\n    sub r2, r0, r1\n\n    add r2, r2, #\'0\'\n    ldr r1, =result\n    strb r2, [r1]\n\n    mov r0, #1\n    ldr r1, =result\n    mov r2, #1\n    mov r7, #4\n    svc #0\n\n    mov r7, #1\n    mov r0, #0\n    svc #0'
    },
    'mul': {
       'x86': 'section .data\n    result db \'0\', 0xA\n    len equ $ - result\n\nsection .text\n    global _start\n\n_start:\n    mov al, 3\n    mov bl, 3\n    mul bl\n\n    cmp ax, 9\n\n    mov bl, 10\n    div bl\n    add ax, \'00\'\n    mov [result], al\n    mov [result+1], ah\n    jmp print_result\n\nsingle_digit:\n    add al, \'0\'\n    mov [result], al\n\nprint_result:\n    mov eax, 4\n    mov ebx, 1\n    mov ecx, result\n    mov edx, len\n    int 0x80\n\n    mov eax, 1\n    xor ebx, ebx\n    int 0x80',
        'mips': '.data\nresult: .asciiz "0\n"\n\n.text\n.globl main\n\nmain:\n    li $t0, 3\n    li $t1, 3\n    mul $t2, $t0, $t1 \n\n    addi $t2, $t2, 48\n    sb $t2, result \n\n    li $v0, 4\n    la $a0, result \n    syscall\n\n    li $v0, 10 \n    syscall',
        'arm': '.section .data\nresult: .asciz "0\\n"\n\n.section .text\n.global _start\n\n_start:\n    mov r0, #3\n    mov r1, #3\n    mul r2, r0, r1\n\n    add r2, r2, #\'0\'\n    ldr r1, =result\n    strb r2, [r1]\n\n    mov r0, #1\n    ldr r1, =result\n    mov r2, #2\n    mov r7, #4\n    svc #0\n\n    mov r7, #1\n    mov r0, #0\n    svc #0'
    },
    'div': {
        'x86': 'section .data\n    result db \'0\', 0xA\n    len equ $ - result\n\nsection .text\n    global _start\n\n_start:\n    mov ax, 10\n    mov bl, 2\n    div bl\n\n    add al, \'0\'\n    mov [result], al\n\n    mov eax, 4\n    mov ebx, 1\n    mov ecx, result\n    mov edx, len\n    int 0x80\n\n    mov eax, 1\n    xor ebx, ebx\n    int 0x80',
        'mips': '.data\n    result: .asciiz "5\\n"\n\n.text\n    .globl main\n\nmain:\n    li $t0, 10\n    li $t1, 2\n    div $t0, $t1\n    mflo $t2\n    addi $t2, $t2, 48\n    sb $t2, result\n    li $v0, 4\n    la $a0, result\n    syscall\n    li $v0, 10\n    syscall',
       'arm': '.data\ndigit: .space 1\nnewline: .byte 10\n\n.text\n.global _start\n\n_start:\n    mov r0, #10\n    mov r1, #2\n    udiv r2, r0, r1\n\n    add r2, r2, #\'0\'\n    ldr r3, =digit\n    strb r2, [r3]\n\n    mov r7, #4\n    mov r0, #1\n    ldr r1, =digit\n    mov r2, #1\n    svc #0\n\n    mov r7, #4\n    mov r0, #1\n    ldr r1, =newline\n    mov r2, #1\n    svc #0\n\n    mov r7, #1\n    mov r0, #0\n    svc #0'
    }
}

@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            return redirect(url_for('dashboard'))

        return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html', error=None)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/x86')
def x86():
    return render_template('x86.html')

@app.route('/mips')
def mips():
    return render_template('mips.html')

@app.route('/arm')
def arm():
    return render_template('arm.html')

@app.route('/playground')
def playground():
    return render_template('playground.html')

@app.route('/architectures')
def architectures():
    return render_template('architectures.html')

@app.route('/question/<question_id>', methods=['GET'])
def code_question(question_id):
    # Just render the basic template - data will be loaded via JS
    return render_template('code_question.html')

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code', '')
    architecture = data.get('architecture', 'x86')
    question_id = data.get('question_id', '')

    try:
        response = requests.post("https://cloud-backend-gp5j.onrender.com/execute", json={
            "code": code,
            "architecture": architecture
        })
        if response.status_code == 200:
            output = response.json().get('output', 'No output received')
        else:
            output = f"Cloud backend error: {response.status_code}"
    except Exception as e:
        output = f"Error contacting cloud backend: {str(e)}"

    # Get the expected output for comparison
    expected_output = questions.get(question_id, {}).get('expectedOutput', '')

    return jsonify({
        'output': output,
        'expected_output': expected_output,  # Include expected output
        'question_id': question_id
    })

@app.route('/api/question/<question_id>')
def api_question(question_id):
    question = questions.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    # Include solution in the response
    solution = solutions.get(question_id, {})
    return jsonify({
        'id': question_id,
        'title': question['title'],
        'description': question['description'],
        'boilerplate': question['boilerplate'],
        'expectedOutput': question['expectedOutput'],  # Add expected output
        'solutions': solution
    })

@app.route('/resources')
def resources():
    return render_template('resources.html')

if __name__ == '__main__':
    app.run(debug=True)
