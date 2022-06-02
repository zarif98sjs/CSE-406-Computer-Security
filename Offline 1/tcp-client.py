from aes import *
from rsa_bv import *
# Import socket module
import socket		
import pickle 	

# Create a socket object
s = socket.socket()		

# Define the port on which you want to connect
port = 12345			

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# recieve [ cipher length ]
c_len = int(s.recv(1024).decode())
print("Length : ", c_len)

# recieve [ ciphers ]
ciphers = []
while True:
  message = s.recv(1024).decode()
  ciphers.append(message)
  if len(ciphers) == c_len:
    break
print(ciphers)

# recieve [ filler count ]
fillerCount = int(s.recv(1024).decode())

# recieve [ encrypted key ]
encryptedKeyString = s.recv(1024)
encryptedKey = pickle.loads(encryptedKeyString)
print("encrypted key : ", encryptedKey)

# recieve [ primary key ]
primaryKeyString = s.recv(1024)
primaryKey = pickle.loads(primaryKeyString)
print("primary key : ", primaryKey)

# read private key from file
with open("DoNotOpenThis/private.key", "rb") as f:
    privateKey = pickle.load(f)

print("private key : ", privateKey)

# decrypt key using private key
decryptedKey = RSADecrypt(privateKey, encryptedKey)
print("decrypted key : ", decryptedKey)

# do aes decryption
decrpytic = AESDecrypt(128, ciphers , decryptedKey, fillerCount)
print(''.join(convertTo1DBitVectorASCII(decrpytic))," [In ASCII]")


# close the connection
s.close()	
	
