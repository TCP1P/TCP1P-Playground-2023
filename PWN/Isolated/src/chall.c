#include <stdio.h>
#include <sys/mman.h>

void setup() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

int main(int argc, char **argv) {
  setup();
  void *exec_addr = mmap(NULL, 0x100, PROT_READ | PROT_WRITE | PROT_EXEC,
                         MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

  char buf[0x100];

  for (int i = 0; i < 3; i++) {
    fgets(buf, sizeof buf, stdin);
    printf(buf);
  }

  void (*shellcode)() = (void (*)())argv[1];
  shellcode();

  return 0;
}
