from ptrlib import *
from fglg import FiniteGeneralLinearGroup as Matrix
import re
import base64
import math
import pickle
import sys

def encrypt(data, p):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("Data: ", base64.b64encode(data))
    return recv_gl(p)

def decrypt(data, p):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter("Data: ", base64.b64encode(data))
    return recv_gl(p)

def recv_gl(p = None):
    sock.recvline()
    mat = []
    for i in range(n):
        mat.append([])
        r = re.findall(b"\d+", sock.recvline())
        for elm in r:
            mat[-1].append(int(elm))
    if p is None:
        return mat
    X = Matrix(n, p)
    for i in range(n):
        for j in range(n):
            X.set_at((j, i), mat[i][j])
    return X

def split(x, base, result):
    if x < base:
        return x
    # x = base ^ q + r
    q = int(math.log(x) / math.log(base))
    r = x - base ** q
    result.append(q)
    return split(r, base, result)

n = 6

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("solve.py gather/solve")
        
    elif sys.argv[1] == 'gather':
        sock = Socket("13.231.224.102", 3002)

        # Get eF and p
        mat = recv_gl()
        sock.recvuntil("p = ")
        p = int(sock.recvline())
        eF = Matrix(n, p)
        for i in range(n):
            for j in range(n):
                eF.set_at((j, i), mat[i][j])

        # Create table
        T = [[None for j in range(n)] for i in range(n)]
        R = [[None for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                data = b'\x00' * (n*n)
                data = data[:i*n+j] + b'\x02' + data[i*n+j+1:]
                T[i][j] = decrypt(data, p)
                data = data[:i*n+j] + b'\x01' + data[i*n+j+1:]
                R[i][j] = decrypt(data, p)
                print("[+] ({}, {})".format(j, i))

        with open("save.wkctf", "wb") as f:
            obj = {}
            obj['p'] = p
            obj['eF'] = eF
            obj['T'] = T
            obj['R'] = R
            pickle.dump(obj, f)
        print("[+] Saved matrices!")
        
    elif sys.argv[1] == 'solve':
        with open("save.wkctf", "rb") as f:
            obj = pickle.load(f)

        R = obj['R']
        T = obj['T']
        p = obj['p']
        eF = obj['eF']
        F = Matrix(n, p)
        X = Matrix(n, p)
        memo = {}
        for i in range(n):
            for j in range(n):
                result = []
                print("[+] Calculating ({}, {})...".format(j, i))
                r = split(eF.get_at((j, i)), 2, result)
                t = -1
                for x in result[::-1]:
                    if (x, j) not in memo:
                        if t == -1:
                            memo[(x, j)] = T[j][j] ** (x - 1)
                        else:
                            memo[(x, j)] = memo[(t, j)] * T[j][j] ** (x - t)
                    t = x
                    F += T[i][j] * memo[(x, j)]
                if r:
                    F += R[i][j]

        flag = ''
        for i in range(n):
            for j in range(n):
                flag += chr(F.get_at((j, i)))

        print(flag)
