FROM python:3.7-alpine

RUN pip3 install Flask

ADD challenge/init.sh             /etc/init.sh
ADD challenge/server/app.py       /root/app.py
ADD challenge/malware/malchan     /root/malchan
ADD challenge/malware/raindrop.sh /root/raindrop.sh

RUN chmod 555 /etc/init.sh
RUN chmod 550 /root/app.py
RUN chmod 440 /root/malchan
RUN chmod 440 /root/raindrop.sh

RUN ls /root -lh
