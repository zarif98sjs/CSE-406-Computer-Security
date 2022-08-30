section .text
  global _start
    _start:
      mov ebx, 0x565562a2
      call ebx
      push eax
      mov ebx, 0x56556286
      call ebx
