from ptrlib import Socket, log
from fractions import Fraction
from math import ceil

log.level = ["warning"]

n = 0x6D70B5A586FCC4135F0C590E470C8D6758CE47CE88263FF4D4CF49163457C71E944E9DA2B20C2CCB0936360F12C07DF7E7E80CD1F38F2C449AAD8ADAA5C6E3D51F15878F456CEEE4F61547302960D9D6A5BDFAD136ED0EB7691358D36AE93AEB300C260E512FAEFE5CC0F41C546B959082B4714F05339621B225608DA849C30F
e = 65537
c = 0x3cfa0e6ea76e899f86f9a8b50fd6e76731ca5528d59f074491ef7a6271513b2f202f4777f48a349944746e97b9e8a4521a52c86ef20e9ea354c0261ed7d73fc4ce5002c45e7b0481bb8cbe6ce1f9ef8228351dd7daa13ccc1e3febd11e8df1a99303fd2a2f789772f64cbdb847d6544393e53eee20f3076d6cdb484094ceb5c1
sig = "3b71ec3d"


def lsb_oracle(e):
    sock = Socket("13.231.224.102", 3001)
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("ENC : ")
    sock.sendline("{:0x}".format(e))
    sock.recvuntil("SIG : ")
    sock.sendline(sig)
    cur_sig = sock.recvline()[-8:]
    return int(cur_sig, 16) & 1


left, right = 0, n
c2 = c
i = 0
while right - left > 1:
    m = Fraction(left + right, 2)
    c2 = (c2 * pow(2, e, n)) % n
    oracle = lsb_oracle(c2)
    if oracle:
        left = m
    else:
        right = m
    if i % 32 == 0:
        print(i)
    i += 1
print(i)
print(int(ceil(left)))
