obj-m := memo.o
#KBUILD_DIR := /lib/modules/$(KVERSION)/build
KBUILD_DIR := /home/ptr/warehouse/buildroot/output/build/linux-4.19.98

all:
	$(MAKE) -C $(KBUILD_DIR) M=$(shell pwd) modules

clean:
	$(MAKE) -C $(KBUILD_DIR) M=$(shell pwd) clean
