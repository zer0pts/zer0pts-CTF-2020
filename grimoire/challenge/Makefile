all:
	gcc -Wl,-z,now,-z,relro main.c -o chall -fstack-protector-all -pie
	cp ./chall ../distfiles/
	cp ./main.c ../distfiles/grimoire.c
	cp /lib/x86_64-linux-gnu/libc.so.6 ../distfiles/
