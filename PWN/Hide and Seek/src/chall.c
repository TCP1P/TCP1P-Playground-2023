#include <stdio.h>
#include <stdlib.h>

__attribute__((constructor)) void setup() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

extern char _start;
void *base;

int main(int argc, char **argv) {
  FILE *flag = fopen("/flag.txt", "r");
  char *buf = (char *)malloc(100);
  fgets(buf, 100, flag);
  fclose(flag);

  base = (void *)((long)&_start & ~0xfff) - 0x1000;
  long offset;

  while (1) {
    printf("Offset: ");
    scanf("%ld%*c", &offset);
    printf("Value: %s\n", (char *)(base + offset));
  }
}
