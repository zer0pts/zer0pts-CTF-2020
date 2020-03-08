from ptrlib import *
import ctypes

glibc = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc-2.27.so')

with open("../distfiles/core", "rb") as f:
    buf = f.read()

ofs_stat = buf.index(p64(0x803))
ofs_tv = ofs_stat - 0x10
ofs_enc = buf.index(p64(0x20db1)) + 8

st_size = u64(buf[ofs_stat + 0x30:ofs_stat + 0x38])
tv_sec = u64(buf[ofs_tv:ofs_tv+8])
tv_usec = u64(buf[ofs_tv+8:ofs_tv+16])
enc = buf[ofs_enc:ofs_enc + st_size]

glibc.srand(tv_sec**2 + tv_usec**2)
plain = b""
for c in enc:
    plain += bytes([c ^ (glibc.rand() & 0xff)])

with open("restored.pdf", "wb") as f:
    f.write(plain)
