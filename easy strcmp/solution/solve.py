import struct

dummy = b"zer0pts{********CENSORED********}"
dummy += b'\x00' * (8 - (len(dummy) % 8))

with open("../distfiles/chall", "rb") as f:
    f.seek(0x1060)
    flag = b""
    for i in range(0, len(dummy), 8):
        x = struct.unpack("<Q", dummy[i:i+8])[0]
        y = struct.unpack("<Q", f.read(8))[0]
        flag += struct.pack("<Q", x + y)
    print(flag.rstrip(b"\x00"))
