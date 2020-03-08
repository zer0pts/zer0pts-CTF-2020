from sage.all import *
from Crypto.Util.number import inverse, long_to_bytes
from re import compile

with open("./../distfiles/output.txt") as f:
    output = f.read()

pubkey = eval(compile(r"pubkey: (.+)\n").findall(output)[0])
shares = eval(compile(r"shares: (.+)\n").findall(output)[0])

ns = []
gs = []
for n, g in pubkey:
    ns.append(n)
    gs.append(g)

# factoring
print("[+] n bits:", [n.bit_length() for n in ns])
m = matrix(ZZ, 5, 5)
m[0, 0] = 2**768
for i in range(1, m.dimensions()[0]):
    m[0, i] = ns[i]
    m[i, i] = -ns[0]
print("[+] matrix")
for i in range(m.dimensions()[0]):
    print(i, [int(x).bit_length() for x in m[i]])

ml = m.LLL()
print("[+] LLL done")
print("[+] matrix")
for i in range(ml.dimensions()[0]):
    print(i, [int(x).bit_length() for x in ml[i]])

# decrypt and get samples of prng
def dec(c, p, q, g):
    n = int(p) * int(q)
    l = int(lcm(p-1, q-1))
    m = ((pow(c, l, n**2)-1) // n) * inverse((pow(g, l, n**2)-1) // n, n)
    k = ((pow(g, l, n**2) - 1) // n) * inverse(l, n)
    return m % n, k % n

q0 = gcd(abs(ml[0][0]), ns[0])
p0 = ns[0] // q0

qs = [q0]
ps = [p0]
res = dec(shares[0][1], p0, q0, gs[0])
ms = [res[0]]
samples = [res[1]]
for i in range(1, 5):
    qi = gcd(abs(ml[0][i])//q0, ns[i])
    pi = ns[i] // qi
    mi, ki = dec(shares[i][1], pi, qi, gs[i])
    qs.append(qi)
    ps.append(pi)
    ms.append(mi)
    samples.append(ki)

# find noises
def bit_reverse(x):
    y = 0
    for i in range(256):
        y = (y << 1) | ((x >> i) & 1)
    return y

s = bit_reverse(samples[-1])
noises = []
idx = 3
for j in range(13):
    x = 0
    for i in range(256):
        msb = s >> 255
        s <<= 1
        lsb = (msb^(s>>0)^(s>>2)^(s>>5)^(s>>10)^1)&1
        s = (s|lsb) & ((1<<256)-1)
        x = (x << 1) | lsb
    noise = bit_reverse(x)
    if j % 3 == 0:
        noises.append(noise)
    elif j % 3 == 2:
        assert noise == samples[idx]
        idx -= 1
noises.reverse()
print("[+] found all noises")

xy = []
for i in range(5):
    xy.append((i+1, ms[i] - noises[i]))

# find PRIME
prev = previous_prime(ps[0])
for x in range(prev, ps[0]):
    prime = x - noises[0]
    if is_prime(prime):
        R = PolynomialRing(GF(prime), name='x')
        f = R.lagrange_polynomial(xy)
        print("[+] flag:", long_to_bytes(f(0)))
