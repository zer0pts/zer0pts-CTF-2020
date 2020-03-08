all:
	gcc -c main.c -o main.o -pie
	gcc -c oget.c -o oget.o -pie
	gcc -Wl,-z,now,-z,relro main.o oget.o -o omega_get -pie
	mv omega_get ../../distfiles/
	cp ./main.c ../../distfiles/src/
	cp ./oget.c ../../distfiles/src/
	cp ./oget.h ../../distfiles/src
	rm *.o
