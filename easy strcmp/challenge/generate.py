import struct

flag  = b"zer0pts{l3ts_m4k3_4_DETOUR_t0d4y}\x00\x00"
dummy = b"zer0pts{********CENSORED********}\x00\x00"
flag += b'\x00' * (8 - (len(flag) % 8))
dummy += b'\x00' * (8 - (len(dummy) % 8))

output = ""
for i in range(0, len(flag), 8):
    a = struct.unpack("<Q", flag[i:i+8])[0]
    b = struct.unpack("<Q", dummy[i:i+8])[0]
    output += "{}, ".format((a - b) % 0x10000000000000000)

print(output)
