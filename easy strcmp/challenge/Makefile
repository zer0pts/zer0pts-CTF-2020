all:
	gcc -Wl,-z,lazy main.c -o chall -fstack-protector -pie -O0 -masm=intel
	strip --strip-all ./chall
	mv ./chall ../distfiles/chall
