obj-m := hobbit.o
#KBUILD_DIR := /lib/modules/`uname -r`/build
KBUILD_DIR := /home/ptr/warehouse/buildroot/output/build/linux-4.19.98

all:
	$(MAKE) -C $(KBUILD_DIR) M=$(shell pwd) modules
	nasm shellcode.S -fELF64

clean:
	$(MAKE) -C $(KBUILD_DIR) M=$(shell pwd) clean
