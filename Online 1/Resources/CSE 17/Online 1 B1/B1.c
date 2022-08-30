#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#define BUF_SIZE <param_1>

int check;
int last_val;

int foo(int a, int b, int session){
    if( session != check){
	printf("Session Terminated. Try Again!\n");
	return 0;
    }
	
    if((a+b) == <param_2> && b!=last_val){	
	printf("Verified session = %d\n", session);
	return 1;
    }
	
    printf("Unauthorized call to foo\n");
    return 0;
}
 
void basic_func(char* str, int a ,int b, int session){
    char buffer1[BUF_SIZE]; 
 	
    printf("Requested session = %d\n", session);
    strcpy(buffer1, str);
    if( !foo(a, b, session) ) exit(1);
}

int main(int argc, char **argv){
    char str[517];
    FILE *badfile;
    
    srand(time(NULL));
    check = rand();
    last_val = rand() % <param_3>;
    
    badfile = fopen("badfile", "r"); 
    if (!badfile) {
       perror("Opening badfile"); exit(1);
    }

    int length = fread(str, sizeof(char), 517, badfile);
    printf("Input size: %d\n", length);
    basic_func(str, 12345, last_val, check);
    fprintf(stdout, "==== Returned Properly ====\n");
    return 1;
}