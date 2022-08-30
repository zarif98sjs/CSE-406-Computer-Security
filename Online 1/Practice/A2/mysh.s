section .text
 global _start
  _start:

xor ecx,ecx
xor eax,eax
mov al,1

mov cl,7
push ecx
push eax
mov ebx,0x56556286
call ebx

xor ecx,ecx
push ecx
push eax
call ebx

mov cl,5
push ecx
push eax
call ebx

xor ecx,ecx
push ecx
push eax
call ebx

mov cl,3
push ecx
push eax
call ebx

xor ecx,ecx
mov cl,7
push ecx
push eax
call ebx
