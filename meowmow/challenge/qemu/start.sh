#!/bin/sh
cd /home/ubuntu/meowmow/challenge/qemu && \
timeout --foreground 300 qemu-system-x86_64 \
    -m 256M \
    -kernel ./bzImage \
    -initrd ./rootfs.cpio \
    -append "root=/dev/ram rw console=ttyS0 oops=panic panic=1 kaslr quiet" \
    -cpu kvm64,+smep,+smap \
    -monitor /dev/null \
    -nographic
