from aes_file_1705010 import *
from rsa_1705010 import *
import socket		
import pickle 

BUFFER_SIZE = 4096 * 10

# Create a socket object
s = socket.socket()		

# Define the port on which you want to connect
port = 12345			

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# recieve [ cipher length ]
c_len = int(s.recv(BUFFER_SIZE).decode())
print("Length : ", c_len)

# recieve [ ciphers ]
ciphers = []
while True:
  message = s.recv(BUFFER_SIZE).decode()
  ciphers.append(message)
  if len(ciphers) == c_len:
    break
print("ciphers : ", ciphers)
print("Length : ", len(ciphers))



# recieve [ encrypted key ]
encryptedKeyString = s.recv(BUFFER_SIZE)
encryptedKey = pickle.loads(encryptedKeyString)
print("encrypted key : ", encryptedKey)

# recieve [ primary key ]
primaryKeyString = s.recv(BUFFER_SIZE)
primaryKey = pickle.loads(primaryKeyString)
print("primary key : ", primaryKey)

# read private key from file
with open("DoNotOpenThis/private.key", "rb") as f:
    privateKey = pickle.load(f)

print("private key : ", privateKey)

# decrypt key using private key
decryptedKey = RSADecrypt(privateKey, encryptedKey)
print("decrypted key : ", decryptedKey)

# recieve [ filler count ]
fillerCount = int(s.recv(BUFFER_SIZE).decode())

decrypted_blob = AESDecrypt(128, ciphers , decryptedKey, fillerCount)
# Write the decrypted contents to a file
fd = open("demo_rev.txt", "wb")
fd.write(decrypted_blob)
fd.close() 
# close the connection
s.close()	
	
