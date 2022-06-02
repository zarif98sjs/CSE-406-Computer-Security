from aes_file_1705010 import *
from rsa_1705010 import *
import socket		
import pickle 

# BUFFER_SIZE = 4096 * 10

# Create a socket object
s = socket.socket()		

# Define the port on which you want to connect
port = 12345			

# connect to the server on local computer
s.connect(('127.0.0.1', port))

class DataToSend:
  def __init__(self,hexStrAra,fillerCount,encryptedKey,publicKey,fileName):
    self.hexStrAra = hexStrAra
    self.fillerCount = fillerCount
    self.encryptedKey = encryptedKey
    self.publicKey = publicKey
    self.fileName = fileName

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

data = pickle.loads(recvall(s))

# read private key from file
with open("DoNotOpenThis/private.key", "rb") as f:
    privateKey = pickle.load(f)

print("private key : ", privateKey)

# decrypt key using private key
decryptedKey = RSADecrypt(privateKey, data.encryptedKey)
print("decrypted key : ", decryptedKey)

decrypted_blob = AESDecrypt(128, data.hexStrAra , decryptedKey, data.fillerCount)
# Write the decrypted contents to a file
fd = open("dec_"+data.fileName, "wb")
fd.write(decrypted_blob)
fd.close() 
# close the connection
s.close()	
	
