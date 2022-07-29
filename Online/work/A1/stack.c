#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int foo(char *str)
{
    int arr[20];
    char buffer[319];

    /* The following statement has a buffer overflow problem */ 
    strcpy(buffer, str);

    return 1;
}

int main(int argc, char **argv)
{
    char str[539];
    FILE *badfile;

    badfile = fopen("badfile", "r");
    fread(str, sizeof(char), 539, badfile);
    foo(str);

    printf("Try Again\n");
    return 1;
}

