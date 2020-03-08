FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install socat
RUN groupadd -r pwn && useradd -r -g pwn pwn

ADD challenge/init.sh        /etc/init.sh
RUN chmod 555  /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm

ADD challenge/howdy_flag.txt /home/pwn/howdy_flag.txt
ADD challenge/chall          /home/pwn/chall
ADD challenge/grimoire.txt   /home/pwn/grimoire.txt
RUN chmod 440 /home/pwn/howdy_flag.txt
RUN chmod 550 /home/pwn/chall
RUN chmod 440 /home/pwn/grimoire.txt

RUN chown -R root:pwn /home/pwn

RUN ls /home/pwn -lh
USER pwn
