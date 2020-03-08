#! /bin/bash
socat TCP-L:9008,reuseaddr,fork EXEC:"/home/pwn/chall",pty,stderr,setsid,sane,raw,echo=0
