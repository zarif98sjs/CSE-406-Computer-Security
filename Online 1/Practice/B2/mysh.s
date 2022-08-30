section .text
 global _start
  _start:
 
mov ebx,0x565562a2
call ebx

mov ecx,0x56556286
push eax
call ecx
