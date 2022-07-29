
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int foo(char *str)
{
    int arr[<param_1>];
    char buffer[<param_2>];

    /* The following statement has a buffer overflow problem */ 
    strcpy(buffer, str);

    return 1;
}

int main(int argc, char **argv)
{
    char str[<param_3>];
    FILE *badfile;

    badfile = fopen("badfile", "r");
    fread(str, sizeof(char), <param_3>, badfile);
    foo(str);

    printf("Try Again\n");
    return 1;
}

