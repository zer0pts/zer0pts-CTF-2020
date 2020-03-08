section .text
global _start

_start:
;; write(1, "FLAG: ", 7);
  mov rdx, 7
  mov rsi, 0xdead0000
  xor eax, eax
  inc eax
  mov rdi, rax
  syscall
;; read(0, buf, 0x100)
  mov rdx, 0x100
  mov rsi, 0xdead00ef
  xor eax, eax
  xor edi, edi
  syscall
;; xor(buf, code, 39);
  cld
  mov rcx, 39
  mov rsi, 0xdead00ef
  mov rdi, rsi
ENCIPHER:
  lodsb
  xor al, cl
  stosb
  loop ENCIPHER
;; memcmp(buf, E"zer0pts{...}", 39);
  mov rcx, 39
  mov rsi, 0xdead0019
  mov rdi, 0xdead00ef
  repe cmpsb
  je CORRECT
WRONG:
  ;; write(1, "Wrong!\n", 8);
  mov rdx, 8
  mov rsi, 0xdead0011
  xor eax, eax
  inc eax
  mov rdi, rax
  syscall
;; exit(0);
EXIT:
  mov rdi, 0
  mov rax, 60
  syscall
CORRECT:
;; write(1, "Correct!\n", 10);
  mov rdx, 10
  mov rsi, 0xdead0007
  xor eax, eax
  inc eax
  mov rdi, rax
  syscall
  jmp EXIT

EOS:
  db 'E', 'O', 'S'
