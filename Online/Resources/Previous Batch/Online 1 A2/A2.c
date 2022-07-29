/* This program has a buffer overflow vulnerability. */
/* Our task is to exploit this vulnerability */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int foo(int a, int b);
int bar(int x);

int bof(char *str)
{
    char buffer[<param_1>];	
    /* The following statement has a buffer overflow problem */ 
    strcpy(buffer, str);
    //printf("Returning from BOF\n");
    return 1;
}


int foo(int a, int b)
{
    int secret = a*10 + b;
    printf("Processing Sensitive Information %d\n",secret);
    return secret;
}

int bar(int x)
{
    printf("Input Parameter %d\n",x);
    return x+1;
}


int main(int argc, char **argv)
{
    char str[<param_2> + 1];
    FILE *badfile;
    badfile = fopen("badfile", "r");
    printf("Inside Main\n");
    fread(str, sizeof(char), <param_2>, badfile);
    bof(str);

    printf("Returned Properly\n");
    return 1;
}