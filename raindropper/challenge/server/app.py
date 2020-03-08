#!/usr/bin/env python
from flask import Flask
import base64

app = Flask(__name__)

@app.route('/raindrop')
def raindrop():
    return open("/root/raindrop.sh", "rb").read()
@app.route('/malchan')
def malchan():
    return base64.b64encode(open("/root/malchan", "rb").read())

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8033,
        debug=False
    )
