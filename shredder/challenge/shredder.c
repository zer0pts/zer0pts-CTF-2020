#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/stat.h>

int sqsum(int a, int b) {
  return a * a + b * b;
}

int shred(char *filename) {
  int fd, i;
  char *buffer;
  struct stat st;
  struct timeval tv;
  struct timezone tz;

  if (stat(filename, &st))
    return 1;

  fd = open(filename, O_RDWR);
  if (fd < 0)
    return 1;

  gettimeofday(&tv, &tz);
  srand(sqsum(tv.tv_sec, tv.tv_usec));
  buffer = malloc(st.st_size);

  lseek(fd, 0, SEEK_SET);
  read(fd, buffer, st.st_size);

  for(i = 0; i < st.st_size; i++) {
    buffer[i] ^= rand() & 0xff;
  }

  lseek(fd, 0, SEEK_SET);
  write(fd, buffer, st.st_size);

  free(buffer);
  close(fd);
  if (unlink(filename) != 0)
    return 1;

  write(1, "Press ENTER to quit...", 0x16);
  read(0, NULL, 1);
  return 0;
}

int main(int argc, char **argv)
{
  signal(SIGALRM, (__sighandler_t)abort);
  alarm(10);

  if (argc >= 2) {
    if (shred(argv[1]))
      abort();
  }

  exit(0);
}
