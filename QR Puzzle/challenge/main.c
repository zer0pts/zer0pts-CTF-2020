#include "main.h"

MAP** load_map(int *size, char *filepath)
{
  MAP **map;
  int i = 0, j;
  *size = -1;
  char line[256];
  FILE *fp = fopen(filepath, "r");

  if (fp == NULL) {
    perror(filepath);
    exit(1);
  }

  while(!feof(fp)) {
    if (fscanf(fp, "%s", line) != 1) break;
    
    if (*size == -1) {
      *size = strlen(line);
      map = (MAP**)malloc(sizeof(MAP*) * (*size));
    } else if (strlen(line) != (*size)) {
      break;
    }
    
    map[i] = (MAP*)malloc(sizeof(MAP) * (*size));

    for(j = 0; j < *size; j++) {
      map[i][j] = line[j] == '0' ? 0 : 1;
    }
    
    i++;
  }

  return map;
}

KEY_CHAIN* load_key(char *filepath)
{
  KEY_CHAIN *kc = NULL, *next;
  FILE *fp = fopen(filepath, "r");
  int dir, x, y;

  if (fp == NULL) {
    perror(filepath);
    exit(1);
  }

  while(1) {
    if (fscanf(fp, "%d#(%d,%d)", &dir, &x, &y) != 3) break;

    next = kc;
    kc = (KEY_CHAIN*)malloc(sizeof(KEY_CHAIN));
    kc->pos.x = x;
    kc->pos.y = y;
    kc->dir = dir;
    kc->next = next;
  }

  return kc;
}

void swapswap(MAP **map, KEY_CHAIN *kc)
{
  int x, y, nx, ny;
  KEY_CHAIN *ptr;
  
  for(ptr = kc; ptr != NULL; ptr = ptr->next) {
    x = nx = ptr->pos.x;
    y = ny = ptr->pos.y;
    switch(ptr->dir) {
    case DIR_LEFT  : nx--; break;
    case DIR_RIGHT : nx++; break;
    case DIR_TOP   : ny--; break;
    case DIR_BOTTOM: ny++; break;
    }
    map[y][x] += map[ny][nx];
    map[ny][nx] = map[y][x] - map[ny][nx];
    map[y][x] -= map[ny][nx];
  }
}

void save_map(MAP **map, int size, char *filepath)
{
  int i, j;
  FILE *fp = fopen(filepath, "w");

  if (fp == NULL) {
    perror(filepath);
    exit(1);
  }
  
  for(i = 0; i < size; i++) {
    for(j = 0; j < size; j++) {
      fprintf(fp, "%d", map[i][j]);
    }
    fprintf(fp, "\n");
  }

  fclose(fp);
}

int main(int argc, char **argv)
{
  KEY_CHAIN *kc;
  MAP **map;
  int size;
  
  if (argc < 4) {
    printf("Usage: %s [qr] [key] [output]\n", argv[0]);
    return 1;
  }

  puts("[+] Loading QR...");
  map = load_map(&size, argv[1]);
  puts("[+] Done!");
  puts("[+] Loading key...");
  kc = load_key(argv[2]);
  puts("[+] Done!");
  puts("[+] Encrypting...");
  swapswap(map, kc);
  puts("[+] Done!");
  puts("[+] Saving encrypted QR...");
  save_map(map, size, argv[3]);
  puts("[+] Done!");
  
  return 0;
}
