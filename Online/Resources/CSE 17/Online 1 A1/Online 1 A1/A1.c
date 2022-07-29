#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#ifndef BUF_SIZE1
#define BUF_SIZE1 367
#endif

int check_a = 72, check_time = 1;
char* str_1;
FILE *badfile;

char code[] =
  "\x31\xc0"             /* xorl    %eax,%eax              */
  "\x50"                 /* pushl   %eax                   */
  "\x68""//sh"           /* pushl   $0x68732f2f            */
  "\x68""/bin"           /* pushl   $0x6e69622f            */
  "\x89\xe3"             /* movl    %esp,%ebx              */
  "\x50"                 /* pushl   %eax                   */
  "\x53"                 /* pushl   %ebx                   */
  "\x89\xe1"             /* movl    %esp,%ecx              */
  "\x99"                 /* cdq                            */
  "\xb0\x0b"             /* movb    $0x0b,%al              */
  "\xcd\x80"             /* int     $0x80                  */
;

int bof(int a, char *guard_str, int time)
{
    int c; char localstr[10] = "Dest";
    c = 6;
    char buffer[BUF_SIZE1];
    strcpy(buffer,localstr);
    printf("In bof %d\n",time);
    strcpy(buffer, guard_str);
    if (a != check_a || time != check_time){
        printf("Try Again.");
        exit(1);
    }
    printf("bof is ending...\n");  
    return 0;
}

int foo(int c, int a, int b){
    printf("%d %d\n",a,b);
    if(a == 768 && b == 68){
        printf("In Foo Successful\n");
        ((void(*)( ))code)( );
    }
    printf("%d %d\n",a,b);
    return 0;
}

int main(int argc, char **argv)
{
    str_1 = (char*)malloc(800 * sizeof(char));

    badfile = fopen("badfile", "r"); 
    if (!badfile) {
       perror("Opening badfile"); 
       exit(1);
    }
    fread(str_1, sizeof(char), 800, badfile);
    bof(check_a, "Normal Test", check_time);
    check_time++;
    bof(check_a, str_1, check_time);
    fprintf(stdout, "==== Returned Properly ====\n");
    return 0;
}