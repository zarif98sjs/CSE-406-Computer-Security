from aes_file import *
# Import socket module
import socket			

# Create a socket object
s = socket.socket()		

# Define the port on which you want to connect
port = 12345			

# connect to the server on local computer
s.connect(('127.0.0.1', port))

c_len = int(s.recv(1024).decode())
print("Length : ", c_len)

ciphers = []
while True:
  # receive data from the server and decoding to get the string.
  message = s.recv(1024).decode()
  ciphers.append(message)

  if len(ciphers) == c_len:
    break
print(ciphers)
fillerCount = int(s.recv(1024).decode())
key = "BUET CSE17 Batch"
decrypted_blob = AESDecrypt(128, ciphers , key, fillerCount)
# Write the decrypted contents to a file
fd = open("demo_rev.txt", "wb")
fd.write(decrypted_blob)
fd.close() 
# close the connection
s.close()	
	
