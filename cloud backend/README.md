## 🚀 CURL Tests

You can test the API directly using `curl` to execute assembly code on the backend. Below are some example requests for `x86`, `MIPS32`, and `ARM` architectures:

### 1. **x86 Assembly Test**

```bash
curl -X POST https://cloud-backend-gp5j.onrender.com/execute \
  -H "Content-Type: application/json" \
  -d '{
    "architecture": "x86",
    "code": "section .data\n    msg db '\''Hello, World!'\'', 0xA\n    len equ $ - msg\n\nsection .text\n    global _start\n\n_start:\n    mov eax, 4\n    mov ebx, 1\n    mov ecx, msg\n    mov edx, len\n    int 0x80\n\n    mov eax, 1\n    xor ebx, ebx\n    int 0x80"
}'
```

### 2. **mips32 Assembly Test**

```bash
curl -X POST https://cloud-backend-gp5j.onrender.com/execute \
  -H "Content-Type: application/json" \
  -d '{
    "architecture": "mips32",
    "code": ".data\n    msg: .asciiz \"Hello, World!\\n\"\n\n.text\n    .globl main\n\nmain:\n    li $v0, 4\n    la $a0, msg\n    syscall\n\n    li $v0, 10\n    syscall"
}'
```

### 3. **ARM Assembly Test**

```bash
curl -X POST https://cloud-backend-gp5j.onrender.com/execute \
  -H "Content-Type: application/json" \
  -d '{
    "architecture": "arm",
    "code": ".data\n    msg: .asciz \"Hello, World!\\n\"\n\n.text\n    .global _start\n\n_start:\n    mov r7, #4\n    mov r0, #1\n    ldr r1, =msg\n    mov r2, #14\n    svc #0\n\n    mov r7, #1\n    mov r0, #0\n    svc #0"
}'
```

---

## Backend Integration Example 🔗

### 1. **Flask**

```python
import requests

def execute_assembly(architecture, code):
    url = 'https://cloud-backend-gp5j.onrender.com/execute'
    payload = {'architecture': architecture, 'code': code}
    response = requests.post(url, json=payload)
    return response.json()
```

### 2. **Node.js**

```javascript
const axios = require('axios');

async function executeAssembly(architecture, code) {
  const response = await axios.post('https://cloud-backend-gp5j.onrender.com/execute', {
    architecture: architecture,
    code: code
  });
  console.log(response.data);
}
```

### 3. **PHP**

```php
<?php
function executeAssembly($architecture, $code) {
    $url = 'https://cloud-backend-gp5j.onrender.com/execute';
    $data = array('architecture' => $architecture, 'code' => $code);
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    return json_decode(curl_exec($ch), true);
}
```

---

### AND MANY MORE...
