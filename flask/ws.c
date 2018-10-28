#include <stdio.h>
#include <unistd.h>

int main() {
    int i;

    // Disable output buffering.
    setbuf(stdout, NULL);

    // for (i = 1; i <= 10; i++) {
    //     printf("%d\n", i);
    //     printf ("вап");
    //     usleep(500000);
    // }

    char name[20];
    printf("Hello. What's your name?\n");
    fgets(name,20,stdin);
    printf("Hi there, %s", name, "\n");

    return 0;
}