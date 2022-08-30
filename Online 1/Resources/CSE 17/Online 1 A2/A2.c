#include <stdlib.h>
#include <stdio.h>
#include <string.h>

/* Changing this size will change the layout of the stack.
 * Instructors can change this value each year, so students
 * won't be able to use the solutions from the past.
 */
#ifndef BUF_SIZE
#define BUF_SIZE1 100
#define BUF_SIZE2 65
#endif

void dummy_function(char *str);
int gl = 0;
char* str_1, *str_2;
FILE *badfile, *badfile_2;

int bof_1(char *str)
{
    char buffer[BUF_SIZE1];
    printf("In bof_1\n");
    strcpy(buffer, str);       
    return 0;
}

char* foo(int a, int b){
	printf("In Foo\n");
	gl = 1;
	if(a == 5 && b == 7){
    		fread(str_2, sizeof(char), 500, badfile_2);
	}
	return str_2;
	
}

int bof_2(char * str){
	if (gl != 1){
		printf("Not Allowed\n");
		return 1;
	}
	char buffer[BUF_SIZE2];
	printf("In bof_2\n");
	strcpy(buffer, str);
	return 0;
}

int main(int argc, char **argv)
{
    str_1 = (char*)malloc(500 * sizeof(char));
    str_2 = (char*)malloc(500 * sizeof(char));

    badfile = fopen("badfile", "r"); 
    badfile_2 = fopen("badfile_2", "r");
    if (!badfile || !badfile_2) {
       perror("Opening badfile"); exit(1);
    }
    fread(str_1, sizeof(char), 500, badfile);
    bof_1(str_1);
    fprintf(stdout, "==== Returned Properly ====\n");
    return 1;
}
