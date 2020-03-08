FROM python:3.7-alpine

RUN apk --no-cache add socat

RUN apk add gcc
RUN apk add musl-dev
RUN apk add gmp-dev
RUN pip install pycrypto

ADD challenge/server.py server.py
ADD challenge/fglg.py   fglg.py
ADD challenge/secret.py secret.py

CMD socat TCP-L:3002,fork,reuseaddr EXEC:"python server.py"
