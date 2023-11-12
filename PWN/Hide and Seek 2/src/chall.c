#include <stdio.h>
#include <sys/mman.h>

__attribute__((constructor)) void setup() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

extern char _start;

int main(int argc, char **argv) {
  FILE *flag = fopen("/flag.txt", "r");
  char *buf = (char *)mmap(0, 0x100, PROT_READ | PROT_WRITE,
                           MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
  fgets(buf, 100, flag);

  void *base = (void *)((long)&_start & ~0xfff) - 0x1000;
  long offset;

  while (1) {
    printf("Offset: ");
    scanf("%ld%*c", &offset);
    printf("Value: %s\n", (char *)(base + offset));
  }
}
