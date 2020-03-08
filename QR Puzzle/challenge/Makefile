all:
	gcc main.c -o chall -O3 -no-pie
	strip --strip-all chall
	./chall flag.map key ../distfiles/encrypted.qr
	cp chall ../distfiles/
	cp key ../distfiles/
