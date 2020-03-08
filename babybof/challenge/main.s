extern read
extern exit
extern setbuf
extern stdin
extern stdout
extern stderr

section .text
global _start

_start:
  call setup
  call main
  call exit

setup:
  push rbp
  mov rbp, rsp
  xor rsi, rsi
  mov rax, stdin
  mov rdi, [rax]
  call setbuf
  mov rax, stdout
  mov rdi, [rax]
  call setbuf
  mov rax, stderr
  mov rdi, [rax]
  call setbuf
  pop rbp
  ret

main:
  push rbp
  mov rbp, rsp
  sub rsp, 0x20
  mov rdx, 0x200
  lea rsi, [rbp-0x20]
  mov rdi, 0
  call read
  leave
  ret

_gift:
  pop r15
  ret
  pop rsi
  ret
