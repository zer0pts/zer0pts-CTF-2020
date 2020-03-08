all:
	g++ -Wl,-z,now,-z,relro main.cpp -o chall -lseccomp -pie -fstack-protector
	cp ./chall    ../distfiles/
	cp ./main.cpp ../distfiles/
