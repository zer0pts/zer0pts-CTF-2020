#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <sys/ptrace.h>
#include <sys/resource.h>
#include <sys/types.h>
#include <sys/user.h>
#include <sys/wait.h>

int is_wrong;
float cursor;
long flag[] = {440402232, 664451175, 394078569, 242108149, 1361453560, 781635187, 75805846, 1933660014, 75805846, 29521129, 75805846, 1669187426, 353663562, 535398750, 535398750, 2250965483, 2002388685, 242108149, 242108149, 1047143526, 50375533, 1516751890, 873889281, 2250965483, 50375533, 75805846, 2250965483, 50375533, 300931661, 1361453560, 242108149, 394078569, 781635187, 353663562, 1516751890, 781635187, 2021659725, 1516891499};

long powm(long base, long exp, long mod) {
  long x;
  if (base == 0) return 0;
  if (exp  == 0) return 1;
  if (exp & 1 == 0) {
    x = powm(base, exp >> 1, mod);
    x = (x * x) % mod;
  } else {
    x = base % mod;
    x = (x * powm(base, exp-1, mod) % mod) % mod;
  }
  return (long)((x + mod) % mod);
}

void inject(int pid, struct user_regs_struct *regs) {
  char c;
  switch(regs->orig_rax) {
  case SYS_fstat:
    is_wrong = 0;
    break;
  case SYS_brk:
    cursor = 0.0;
    break;
  case SYS_write:
    c = ptrace(PTRACE_PEEKDATA, pid, regs->rsi, NULL) & 0xff;
    regs->rdx = 1;
    is_wrong |= powm(c, 23531, 2343464867) - flag[(int)cursor];
    cursor += 0.5;
    break;
  case SYS_exit_group:
    if (is_wrong) {
      puts("Wrong!");
    } else {
      puts("Correct!");
    }
    break;
  }
  syscall(SYS_ptrace, PTRACE_SETREGS, pid, NULL, regs);
}

__attribute__ ((constructor)) void __daemon(void) {
  struct rusage usage;
  struct user_regs_struct regs;
  int pid, s;
  pid = syscall(SYS_fork);
  if (pid == 0) {
    syscall(SYS_ptrace, PTRACE_TRACEME, 0, 0, 0);
    syscall(SYS_kill, syscall(SYS_getpid), SIGSTOP);
  } else {
    syscall(SYS_wait4, pid, &s, 0, &usage);
    syscall(SYS_ptrace, PTRACE_SETOPTIONS, pid, NULL, PTRACE_O_TRACESYSGOOD);
    while(1) {
      syscall(SYS_ptrace, PTRACE_SYSCALL, pid, NULL, NULL);
      syscall(SYS_wait4, pid, &s, 0, &usage);
      if (WIFSTOPPED(s) && (WSTOPSIG(s) & 0x80)) {
        syscall(SYS_ptrace, PTRACE_GETREGS, pid, NULL, &regs);
        inject(pid, &regs);
      }
      if (WIFEXITED(s)) syscall(SYS_exit_group, 0);
    }
  }
}

int main(int argc, char **argv) {
  if (argc == 2) {
    puts(argv[1]);
  } else {
    puts("Feed me flag");
  }
  return 0;
}
