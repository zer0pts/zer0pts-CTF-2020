all:
	musl-gcc main.c -o chall -fno-stack-protector -no-pie -O3 -static
	strip --strip-all ./chall
	mv chall ../distfiles
	cp main.c ../distfiles/main.c
