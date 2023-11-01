#include <stddef.h>
#include <stdio.h>
#include <unistd.h>

void setup() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

void vuln() {
  char name[0x40];
  char answer[0x100];

  printf("What's your name? ");
  read(STDIN_FILENO, name, sizeof(name));
  printf("Hello, %s\nWhat is binary exploitation? ", name);
  gets(answer);
  printf("Thank you for your answer!\n");
}

int main() {
  setup();
  vuln();
  return 0;
}
