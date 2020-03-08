from ptrlib import u32, u64
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

with open("../challenge/chall.hbt", "rb") as f:
    f.seek(0x8)
    key_data = f.read(16)
    key_text = f.read(16)
    f.seek(0x28)
    len_data = u32(f.read(4))
    f.seek(0x34)
    len_text = u32(f.read(4))
    f.seek(0x40)
    data = f.read(len_data)
    text = f.read(len_text)

output = ''
for i, c in enumerate(RC4(data, key_data)[0x19:]):
    output += chr(c ^ (39 - i))

print(output)
