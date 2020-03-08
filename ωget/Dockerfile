FROM ubuntu:18.04

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install python python-flask --fix-missing
RUN groupadd -r pwn && useradd -r -g pwn pwn

ADD challenge/flag.txt             /home/pwn/woa_u_got_flag.txt
ADD challenge/omega_get            /home/pwn/omega_get
ADD challenge/server/app.py        /home/pwn/server/app.py
ADD challenge/server/templates/    /home/pwn/server/templates/
ADD challenge/init.sh              /etc/init.sh

RUN chmod 550 /home/pwn/omega_get
RUN chmod 440 /home/pwn/woa_u_got_flag.txt
RUN chmod 440 /home/pwn/server/templates/index.html
RUN chmod 550 /home/pwn/server/app.py

RUN chown -R root:pwn /home/pwn

RUN ls /home/pwn -lh
RUN chmod 700 /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm
