#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void setup() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

int main(int argc, char **argv) {
  setup();
  int num;
  int jackpot;
  char buf[0x100];

  do {
    srand(time(0));
    int x = rand() * rand();
    printf("Give me your number: ");
    scanf("%d%*c", &num);
    jackpot = (x - num) == 777;
    if (jackpot) {
      printf("Jackpot!!! What do you want to say? ");
      fgets(buf, sizeof(buf), stdin);
      printf("You say: ");
      printf(buf);
      putchar(10);
    }
  } while (jackpot);
  printf("You lose, Bye!\n");
  exit(0);
}
