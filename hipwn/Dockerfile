FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install xinetd
RUN groupadd -r pwn && useradd -r -g pwn pwn

ADD challenge/pwn.xinetd /etc/xinetd.d/pwn
ADD challenge/init.sh    /etc/init.sh
ADD challenge/redir.sh   /home/pwn/redir.sh
RUN chmod 550        /home/pwn/redir.sh
RUN chmod 700        /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm

ADD challenge/flag.txt /home/pwn/flag.txt
ADD distfiles/chall    /home/pwn/chall
RUN chmod 440 /home/pwn/flag.txt
RUN chmod 550 /home/pwn/chall

RUN chown -R root:pwn /home/pwn

RUN ls /home/pwn -lh

RUN service xinetd restart
