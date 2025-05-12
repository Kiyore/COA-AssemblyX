document.addEventListener('DOMContentLoaded', async () => {
    // Get question ID from URL
    const pathParts = window.location.pathname.split('/');
    const questionId = pathParts[pathParts.length - 1];
    
    // Try to get from session storage first
    const sessionQuestion = JSON.parse(sessionStorage.getItem('currentQuestion') || '{}');
    if (sessionQuestion.id === questionId) {
      document.getElementById('question-title').textContent = sessionQuestion.title;
    }

    // Load question data
    try {
      const response = await fetch(`/api/question/${questionId}`);
      if (!response.ok) throw new Error('Question not found');
      
      const question = await response.json();
      
      // Update UI
      document.getElementById('question-title').textContent = question.title;
      document.getElementById('question-description').textContent = question.description;
      document.getElementById('code-editor').value = question.boilerplate;
      
      // Store solutions globally
      window.currentQuestion = {
        id: questionId,
        title: question.title,
        solutions: question.solutions || {}
      };
      
    } catch (error) {
      console.error('Failed to load question:', error);
      document.getElementById('question-title').textContent = 'Error loading question';
    }

    // Solution button handler
    document.getElementById('solution-btn').addEventListener('click', (e) => {
      e.preventDefault();
      const solutionBox = document.getElementById('solution-box');
      const arch = document.querySelector('.architecture-select').value;
      
      if (solutionBox.style.display === 'none') {
        const solution = window.currentQuestion?.solutions[arch] || 
                        window.currentQuestion?.solutions[arch.replace('32', '')] || 
                        'No solution available for this architecture';
        solutionBox.textContent = solution;
        solutionBox.style.display = 'block';
      } else {
        solutionBox.style.display = 'none';
      }
    });

    // Form submission handler
    
    

    // Architecture switcher
    document.querySelector('.architecture-select').addEventListener('change', function() {
      const arch = this.value;
      const boilerplates = {
        x86: `section .text\n    global _start\n\n_start:\n    ; Your x86 code here\n    mov eax, 1\n    mov ebx, 0\n    int 0x80`,
        mips32: `.text\n.globl main\n\nmain:\n    # Your MIPS32 code here\n    li $v0, 10\n    syscall`,
        arm: `.text\n.global _start\n\n_start:\n    @ Your ARM code here\n    mov r7, #1\n    svc 0`
      };
      document.getElementById('code-editor').value = boilerplates[arch] || '';
    });
  });