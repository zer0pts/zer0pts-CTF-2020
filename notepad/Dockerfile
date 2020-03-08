FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install python3 python3-pip
RUN pip3 install Flask
RUN pip3 install flask-bootstrap
RUN groupadd -r web && useradd -r -g web web

ADD challenge/flag                 /home/web/flag
ADD challenge/app.py               /home/web/app.py
ADD challenge/templates/index.html /home/web/templates/index.html
ADD challenge/init.sh              /etc/init.sh

RUN chown -R root:root /home/web
RUN chown root:root /home/web
RUN chmod 644 /home/web/flag
RUN chmod 755 /home/web/templates
RUN chmod 644 /home/web/templates/index.html
RUN chmod 755 /home/web/app.py

RUN chmod 555 /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm
USER web

RUN ls /home/web -lh
RUN whoami
    
