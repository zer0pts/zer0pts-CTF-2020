#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DIR_LEFT   0
#define DIR_RIGHT  1
#define DIR_TOP    2
#define DIR_BOTTOM 3

typedef struct {
  int x;
  int y;
} POSITION;

typedef int DIRECTION;

typedef struct _KEY_CHAIN {
  POSITION pos;
  DIRECTION dir;
  struct _KEY_CHAIN *next;
} KEY_CHAIN;

typedef char MAP;
