from email import message
from aes_file_1705010 import *        
from rsa_1705010 import *
import socket,pickle,os 

#############################################
#############################################

key = "BUET CSE17 Batch"
fName = "demo.txt"
fd = open(fName, "rb")
unencrypted_blob = fd.read()
print(len(unencrypted_blob))
fd.close()

#############################################
#############################################

 
# next create a socket object
s = socket.socket()        
print ("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345               
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))        
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(5)    
print ("socket is listening")      


# do aes encryption on unencrypted_blob
hexStrAra, fillerCount =  AESEncrypt(128, unencrypted_blob , key)

# generate keys for RSA
keyLength = 32
p1 , p2 = generatePrimes(keyLength//2)
publicKey , privateKey = generateKeyPair(p1,p2)

print("public key : ", publicKey)
print("private key : ", privateKey)

# write private key to file
privateKeyFileName = "DoNotOpenThis/private.key"
os.makedirs(os.path.dirname(privateKeyFileName), exist_ok=True)
with open(privateKeyFileName, "wb") as f:
    pickle.dump(privateKey, f)

# do RSA on key, make encrypted key
encryptedKey = RSAEncrypt(publicKey, key)

class DataToSend:
  def __init__(self,hexStrAra,fillerCount,encryptedKey,publicKey,fileName):
    self.hexStrAra = hexStrAra
    self.fillerCount = fillerCount
    self.encryptedKey = encryptedKey
    self.publicKey = publicKey
    self.fileName = fileName

data = DataToSend(hexStrAra,fillerCount,encryptedKey,publicKey,fName)
 
# a forever loop until we interrupt it or
# an error occurs
while True:
 
  # Establish connection with client.
  c, addr = s.accept()    
  print ('Got connection from', addr )

  with c:
    encryptedData = pickle.dumps(data)
    c.sendall(encryptedData)
    print('data sent')

  # Close the connection with the client
  c.close()
   
  # Breaking once connection closed
  break