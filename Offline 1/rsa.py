import random
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

    print("Public key: ",e)
    print("Private key: ",d)

    return ((e,n),(d,n))

def encrypt(privateKey,text):
    key , n = privateKey
    ciphers = []
    for ch in text:
        ciphers.append((ord(ch) ** key) % n)
    return ciphers

def decrypt(publicKey,ciphers):
    key , n = publicKey
    plaintext = ""
    for cipher in ciphers:
        plaintext += chr((cipher ** key) % n)
    return plaintext

def main():
    keyLength = 16
    p1 , p2 = generatePrimes(keyLength//2)
    # print integer value
    # print(p1.int_val())
    # print(p2.int_val())

    publicKey , privateKey = generateKeyPair(p1,p2)
    text = "hello        world"
    ciphers = encrypt(privateKey,text)
    print(ciphers)
    plaintext = decrypt(publicKey,ciphers)
    print(plaintext)


    # bv1 = BitVector(intVal = 2)
    # bv2 = BitVector(intVal = 7)
    # bv3 = bv1.gf_multiply(bv2)
    # print(bv3.int_val())


main()