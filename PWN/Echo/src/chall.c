#include <stdio.h>

void setup() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

int main(int argc, char **argv) {
  setup();
  char buf[0x100];
  while (1) {
    fgets(buf, sizeof(buf), stdin);
    printf(buf);
  }
}
