#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#define BUF_SIZE_1 <param_1>
#define BUF_SIZE_2 <param_2>
#define BUF_SIZE_3 <param_3>

int myfunc1(char* str){
    int i = 7;
    char buffer1[BUF_SIZE_1];
    strcpy(buffer1, str);
}

int myfunc2(char* str){
    char s[21] = "Hello World";
    char buffer2[BUF_SIZE_2];
    strcpy(buffer2, str);
}

int myfunc3(char* str){
    double d = 71.69;
    char buffer3[BUF_SIZE_3];
    strcpy(buffer3, str);
}

int bof(char *str){
    char buffer1[BUF_SIZE_1];
    char buffer2[BUF_SIZE_2];
    char buffer3[BUF_SIZE_3];

    int choice;
    scanf("%d",&choice);
	
    switch(choice){
        case 1:{
            myfunc1(str);
            break;
        }
        case 2:{
            myfunc2(str);
            break;
        }
        default:{
            myfunc3(str);
        }
    }  
    return 1;
}

int main(int argc, char **argv){
    char str[517];
    FILE *badfile;

    myfunc1("Normal Execution");
    myfunc2("Normal Execution");
    myfunc3("Normal Execution");
    
    badfile = fopen("badfile", "r"); 
    if (!badfile) {
        perror("Opening badfile"); exit(1);
    }

    int length = fread(str, sizeof(char), 517, badfile);
    printf("Input size: %d\n", length);
    bof(str);
    fprintf(stdout, "==== Returned Properly ====\n");
    return 1;
}
