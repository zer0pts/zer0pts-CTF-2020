from ptrlib import *

p = 42821
q = 54727
e = 0x5BEB
N = p * q
phi = (p - 1) * (q - 1)
d = inverse(e, phi)

with open("../distfiles/wysinwyg", "rb") as f:
    f.seek(0x2020)
    flag = b''
    for i in range(38):
        flag += bytes([pow(u64(f.read(8)), d, N)])
    print(flag)
