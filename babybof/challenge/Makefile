all:
	nasm -f elf64 -o chall.o main.s
	ld -dynamic-linker /lib64/ld-linux-x86-64.so.2 -o chall -lc chall.o script.ld -z noexecstack -z now -z relro
	rm chall.o
	mv chall ../distfiles/
