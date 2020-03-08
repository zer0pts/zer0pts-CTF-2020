flag = 0

with open("../distfiles/chall.txt", "r") as f:
    for i, line in enumerate(f):
        x = int(line)
        if x % 2**100 != 0:
            flag |= 1 << i

print(bytes.fromhex(hex(flag)[2:]))
