## 🚀 AssemblyX - Learn & Run Assembly Code Online

**AssemblyX** is a lightweight online platform to **write**, **run**, and **test** assembly programs in **x86**, **MIPS32**, and **ARM** architectures. Built for simplicity and learning, it lets users write assembly code and instantly view the output — all from the browser.

---

## 🔗 Useful Links
 **(Note that using any of the link for the first time may take some time as render put application in sleep due to inactivity)**
- 🌐 **AssemblyX Web App**  
  https://coa-hr8m.onrender.com  (Login credentials: Username - test, Password - 123)
- ⚙️ **Custom Flask API Server**  
  https://cloud-backend-gp5j.onrender.com

> 📌 You can reuse this server in your own projects if not the whole site because there is no publically available API keys to handle this three `x86`,`mips32`,`ARM`.
> You can integrate it in any backend script like `flask`,`node.js`,`php`etc  Just like any other API.
> 
> More Help available in README of cloud_backned
> [Link to Backend README](./cloud%20backend/README.md)


---

## ⚙️ Tech Stack

- **Flask** – for routing and rendering pages
- **Custom Flask API (Cloud_Backend)** – to compile and run user-submitted assembly code

---

## ⚠️ Important Note

`cloud_backend.py` is the core API that compiles and executes code for:
 `x86`,
 `mips32`,
 `ARM`

⚠️ **Must run on a Linux-based environment**, as it uses platform-specific compilers and commands.

📦 `requirements.txt` and a `Dockerfile` are included to help with setup and deployment.

---

## 📚 Learning + Practice

- Supports the learing of `x86`,`ARM`,`mips32` by providing some brief, questions that can be answered prefered language
- View solutions if stuck
- Explore curated external learning resources

> ⚠️ Assembly is tricky — no helpful error logs, just silent crashes. Knowing the assembler/emulator used is crucial.

---

## 🛠️ Architecture & Toolchain

| Architecture | Assembler & Emulator                   | Notes                              |
|--------------|----------------------------------------|------------------------------------|
| `x86`        | `nasm` + `ld` + native Linux execution | 32-bit ELF binaries (Linux only)   |
| `mips32`     | `spim`                                 | MIPS syscall-based programs        |
| `arm`        | `arm-linux-gnueabi-as/ld` + `qemu-arm` | Uses Linux syscalls like `svc #0`  |

---

## 🔧 Additional Features

Features that I failed to add because of time constraints and that anyone reading this can add are:

1. Small animations of data movement in the registers and operations taking place for each line of the solutions that is provided. If you complete this, you can go a bit advanced and try creating dynamic animations for whatever code the user writes.  
2. A random fact bar where you can get a new assembly fact every time you click on it, along with a link if available.  
3. Currently, the questions and solutions are hardcoded in the Flask script — fine for small scale. But for more questions, we could add a separate admin login to manage them dynamically.  

**Also, the login is of no use in this build, since no data is being stored for any user.**

> "Anyways, these are some additions that I wished I could have added, but due to time constraints, I failed. Else, you have the internet and your imagination — you can add this or anything else as add-ons for this web app."
