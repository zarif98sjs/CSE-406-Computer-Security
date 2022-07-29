import random, time
from BitVector import *

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

def encrypt(publicKey,text):
    key , n = publicKey
    ciphers = []
    for ch in text:
        ciphers.append(bigMod(ord(ch),key,n))
    return ciphers

def decrypt(privateKey,ciphers):
    key , n = privateKey
    plaintext = ""
    for cipher in ciphers:
        plaintext += chr(bigMod(cipher,key,n))
    return plaintext

def RSAEncrypt(publicKey,text):
    ciphers = encrypt(publicKey,text)
    return ciphers

def RSADecrypt(privateKey,ciphers):
    plaintext = decrypt(privateKey,ciphers)
    return plaintext

def main():
    
    # keyLengths = [16,32,64,128]
    keyLengths = [512]
    for keyLength in keyLengths:
        print("Key length: ",keyLength)
        start_time = time.time()
        p1 , p2 = generatePrimes(keyLength//2)
        publicKey , privateKey = generateKeyPair(p1,p2)
        key_generation_time = time.time() - start_time
        

        text = "helloworld"*100
        start_time = time.time()
        ciphers = encrypt(publicKey,text)
        encryption_time = time.time() - start_time
        # print(ciphers)

        start_time = time.time()
        plaintext = decrypt(privateKey,ciphers)
        decryption_time = time.time() - start_time
        # print(plaintext)

        print("Key generation time: ",key_generation_time)
        print("Encryption time: ",encryption_time)
        print("Decryption time: ",decryption_time)

# main()