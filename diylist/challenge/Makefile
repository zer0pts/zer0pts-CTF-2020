all:
	gcc -shared diylist.c -o libdiylist.so -fPIC
	gcc main.c -o chall -L./ -ldiylist -no-pie
	strip --strip-all chall
	cp chall ../distfiles/
	cp libdiylist.so ../distfiles/
	cp diylist.c ../distfiles/
	cp diylist.h ../distfiles/
	cp main.c    ../distfiles/

test:
	LD_LIBRARY_PATH=./ ./chall
