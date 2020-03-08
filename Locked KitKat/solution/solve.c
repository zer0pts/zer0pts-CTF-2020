#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
#define MAX_LENGTH 9

void sha1(unsigned char *data, unsigned char *hash, int len) {
  SHA_CTX c;
  SHA1_Init(&c);
  SHA1_Update(&c, data, len);
  SHA1_Final(hash, &c);
}

long crack(unsigned char *target, int len, int depth, unsigned long code) {
  int i;
  long result;
  unsigned long c = code;
  unsigned char hash[SHA_DIGEST_LENGTH];
  unsigned char data[MAX_LENGTH];

  if (depth == len) {
    for (i = 0; i < len; i++) {
      data[i] = c % 10;
      c /= 10;
    }
    sha1(data, hash, len);
    if (strncmp(target, hash, SHA_DIGEST_LENGTH) == 0) {
      return code;
    } else {
      return -1;
    }
  } else {
    for (i = 0; i < 10; i++) {
      result = crack(target, len, depth + 1, code * 10 + i);
      if (result != -1) break;
    }
  }

  return result;
}

int main(void) {
  int l, i;
  unsigned char target[SHA_DIGEST_LENGTH];
  long result;
  FILE *fp = fopen("./gesture.key", "rb");
  if (fp == NULL) {
    perror("gesture.key");
    return 1;
  }

  l = fread(target, SHA_DIGEST_LENGTH, 1, fp);

  for(l = 1; l <= MAX_LENGTH; l++) {
    result = crack(target, l, 0, 0);
    if (result == -1) {
      printf("[-] Failed: len=%d\n", l);
    } else {
      printf("Code: ");
      for(i = 0; i < l; i++) {
        printf("%c", (char)(0x30 + (result % 10)));
        result /= 10;
      }
      putchar('\n');
      fclose(fp);
      return 0;
    }
  }

  puts("Solution not found :(");
  fclose(fp);
  return 1;
}
