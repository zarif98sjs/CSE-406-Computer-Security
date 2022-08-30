import random
import zlib
from BitVector import *
import base64

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def generatePrime(bits):
    # Generate a random prime number of the specified bit length.
    bv = BitVector(intVal = 0)
    check = 0
    while check < 0.999:
        bv = bv.gen_random_bits(bits)  
        check = bv.test_for_primality()
    return bv    

def generatePrimes(bits):
    p1 = generatePrime(bits)
    p2 = generatePrime(bits)
    while p2 == p1:
        p2 = generatePrime(bits)
    return p1.int_val(),p2.int_val()

def generateKeyPair(p,q):
    n = p * q
    phi = (p-1) * (q-1)
    
    e = random.randrange(1,phi)
    g = gcd(e,phi)
    while g != 1:
        e = random.randrange(1,phi)
        g = gcd(e,phi)

    d = modinv(e,phi)
    
    return ((e,n),(d,n))

def bigMod(x,n,mo):
    if n == 0:
        return 1
    u = bigMod(x,n//2,mo)
    u = (u * u) % mo
    if n % 2 == 1:
        u = (u * x) % mo
    return u

def encryptFile(publicKey,text):
    key , n = publicKey
    ciphers = []
    for ch in text:
        ciphers.append(bigMod(ch,key,n))
    return ciphers

def decryptFile(privateKey,ciphers):
    key , n = privateKey
    plaintext = []
    for cipher in ciphers:
        plaintext.append(bigMod(cipher,key,n))
    return bytes(plaintext)

def main():

    fd = open("square.png", "rb")
    unencrypted_blob = fd.read()
    fd.close()

    keyLength = 16
    p1 , p2 = generatePrimes(keyLength//2)

    publicKey , privateKey = generateKeyPair(p1,p2)
    print("Public Key: ", publicKey)
    print("Private Key: ", privateKey)
    print("")
    ciphers = encryptFile(publicKey,unencrypted_blob)
    print(len(ciphers))
    decrypted_blob = decryptFile(privateKey,ciphers)
    print(len(decrypted_blob))

    print(unencrypted_blob[0:10])
    print(decrypted_blob[0:10])

    # Write the decrypted contents to a file
    fd = open("square_rev.png", "wb")
    fd.write(decrypted_blob)
    fd.close()  

main()