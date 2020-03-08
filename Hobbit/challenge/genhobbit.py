from ptrlib import p32, p64, xor
import os

def KSA(key):
    S = [i for i in range(0x100)]
    j = 0
    for i in range(0x100):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S
    
def PRGA(S):
    i, j = 0, 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def RC4(data, key):
    S = KSA(key)
    gen = PRGA(S)
    data = bytearray(data)
    result = bytearray(c ^ n for c, n in zip(data, gen))
    return result

with open("shellcode.o", "rb") as f:
    f.seek(0x180)
    code = f.read()
    code = code[:code.find(b'EOS')]

flag = b'zer0pts{d33ds_w1ll_n0t_b3_l3ss_v4l14nt}'
for i in range(len(flag)):
    flag = flag[:i] + bytes([flag[i] ^ (39 - i)]) + flag[i+1:]

data_key = os.urandom(16)
text_key = os.urandom(16)

data  = b'FLAG: \0'
data += b'Correct!\n\0'
data += b'Wrong!\n\0'
data += flag

buf  = b'HOBBIT\x01\x02'
buf += data_key
buf += text_key
buf += p32(len(data))
buf += p64(0xdead0000)
buf += p32(len(code))
buf += p64(0xbeef0000)
buf += RC4(data, data_key)
buf += RC4(code, text_key)

with open("hoge.hbt", "wb") as f:
    f.write(buf)
