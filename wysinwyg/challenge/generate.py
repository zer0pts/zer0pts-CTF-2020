flag = b'zer0pts{sysc4ll_h00k1ng_1s_1mp0rt4nt}\n'

p = 54727
q = 42821
e = 23531
N = p * q
print(N)

for c in flag:
    d = pow(c, e, N)
    print("{}, ".format(d), end="")
