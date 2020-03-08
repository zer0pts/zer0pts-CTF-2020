import qrcode

qr = qrcode.QRCode(
    box_size=1,
    border=0
)
qr.add_data('zer0pts{puzzl3puzzl3}')
qr.make()

output = ''
img = qr.make_image()
for y in range(img.size[1]):
    for x in range(img.size[0]):
        output += '1' if img.getpixel((x, y)) == 0 else '0'
    output += '\n'
print(output.strip())
