all:
	gcc -Wl,-z,now,-z,relro shredder.c -o shredder -fstack-protector -pie
	strip --strip-all shredder
