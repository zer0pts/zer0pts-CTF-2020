#include <stdio.h>
#include <string.h>
#define ROL(v) (((unsigned long)(v)&0xffffffff)<<32)|((unsigned long)(v)>>32)

unsigned long delta[] = {
  0, 4686632258374338882, 796841318371695088, 5695428477452625963, 0
};
int (*__strcmp)(const char*, const char*);

int __detour(char *s1, const char *s2) {
  int len, i;
  for(len = 0; s1[len]; len++);
  len >>= 3;
  len++;
  for(i = 0; i < len; i++) {
    *(unsigned long*)(&s1[i << 3]) -= delta[i];
  }
  return __strcmp(s1, s2);
}

__attribute__((constructor)) void initialize() {
  asm volatile(".intel_syntax noprefix;"
               "call popper;"
               "popper:"
               "pop rdx;"
               "sub rdx, 0x79e;"
               "mov rdi, rdx;"
               "add rdi, 0x201028;"
               "mov rax, [rdi];"
               "mov [rdx + 0x201090], rax;"
               "add rdx, 0x6ea;"
               "mov [rdi], rdx;");
}

int main(int argc, char **argv) {
  if (argc < 2) {
    printf("Usage: %s <FLAG>\n", argv[0]);
  } else if (strcmp(argv[1], "zer0pts{********CENSORED********}") == 0) {
    puts("Correct!");
  } else {
    puts("Wrong!");
  }
  return 0;
}
