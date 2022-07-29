# aes encryption
from BitVector import *
import time
import codecs

roundD = {128 : 10, 192 : 12, 256 : 14}
DEBUG = 0
ROW = 4

b0 = BitVector(hexstring="00")
b2 = BitVector(hexstring="02")

AES_modulus = BitVector(bitstring='100011011') # Used in gf_multiply_modular()

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]

# left shift a row n times
def leftShift1D(row,n):
    for _ in range(n):
        row.append(row.pop(0))
    return row

def leftShift2D(mat):
    for i in range(ROW):
        mat[i] = leftShift1D(mat[i],i)
    return mat


# right shift a row n times
def rightShift1D(row,n):
    for _ in range(n):
        row.insert(0,row.pop())
    return row

def rightShift2D(mat):
    for i in range(ROW):
        mat[i] = rightShift1D(mat[i],i)
    return mat

# substitute bytes 1D
def subBytes1D(row,isInv=False):
    ret = []
    if isInv:
        for el in row:
            ret.append(BitVector(intVal=InvSbox[el.intValue()], size=8))
    else:
        for el in row:
            ret.append(BitVector(intVal=Sbox[el.intValue()], size=8))
    return ret

# substitute bytes 2D
def subBytes2D(mat,isInv=False):
    ret = []
    for row in mat:
        ret.append(subBytes1D(row,isInv))
    return ret


def xor1D(a,b):
    ret = []
    for i in range(len(a)):
        ret.append(a[i] ^ b[i])
    return ret

def xor2D(a,b):
    ret = []
    for i in range(len(a)):
        ret.append(xor1D(a[i],b[i]))
    return ret

def g__ (row,roundConst):
    ret = leftShift1D(row,1)
    ret = subBytes1D(ret)
    ret = xor1D(ret,[roundConst,b0,b0,b0])
    return ret

def MixColumns(COL,mat,isEncryptMode=True):
    ret = []
    for _ in range(ROW):
        ret.append([BitVector(intVal=0, size=8)] * COL)

    if isEncryptMode:
        mixer = Mixer
    else:
        mixer = InvMixer

    for i in range(ROW):
        for j in range(COL):
            for k in range(ROW):
                ret[i][j] ^= mixer[i][k].gf_multiply_modular(mat[k][j], AES_modulus, 8)

    return ret

# def convertTo2DHexArray(hexArray):
#     twoDArray = []
#     for i in range(0,len(hexArray),4):
#         twoDArray.append(hexArray[i:i+4])
#     return twoDArray

def convertTo2DHexArray(hexArray):
    retMatrix = [] # A 2D list to contain the words of "byteArray" in column-major order
    length = len(hexArray)
    for k in range(4):
        row = []
        for i in range(k, length, 4):
            row.append(BitVector(hexstring=hexArray[i]))
        retMatrix.append(row)
    return retMatrix

def convertTo1DHexArray(content):
    hexArray = []
    for i in range(len(content)):
        hexArray.append(content[i].encode().hex())
    return hexArray


"""
trims or pads key
"""
def processKey(aesLen,key):
    keyLen = aesLen//8
    key = key[:keyLen]
    key = key.ljust(keyLen, '0')
    # print(key)
    # print(key.encode().hex())
    key1D = convertTo1DHexArray(key)
    # print(key1D)
    return key1D
    

"""
AES key scheduling
"""
def generateKey(aesLen,key):

    allKeys = []
    # print("key: ", key)
    keyInit = convertTo2DHexArray(key)
    allKeys.append(keyInit)

    COL = aesLen // 32        # Matrix column
    # print("COL: ", COL)
    
    roundConst = BitVector(hexstring="01")
    for round in range(1,roundD[aesLen]+1):
        lastRow = []
        for i in range(4):
            lastRow.append(allKeys[round-1][i][COL-1]) ## last one
        lastRow = g__(lastRow,roundConst)

        curKey = []
        for col in range(COL):
            prevRowToXor = []
            for i in range(4):
                prevRowToXor.append(allKeys[round-1][i][col])
            prevRowToXor = xor1D(prevRowToXor,lastRow)
            curKey.append(prevRowToXor)
            lastRow = prevRowToXor

        # transpose curKey
        transposedKey = []
        for i in range(4):
            row = []
            for j in range(COL):
                row.append(curKey[j][i])
            transposedKey.append(row)
        
        allKeys.append(transposedKey)

        roundConst = b2.gf_multiply_modular(roundConst, AES_modulus, 8) # round_constant = 2 * round_constant (with MOD)

    return allKeys

def printAllKeys(allKeys):
    for i in range(len(allKeys)):
        print("Round ", i)
        print2DBitVectorHex(allKeys[i])
        print("---------------")
        print("\n")

def print2DBitVectorHex(mat):
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            print(mat[i][j].get_bitvector_in_hex(), end=' ')
        print("\n")       

def print2DBitVectorASCII(mat):
    R = len(mat)
    C = len(mat[0])
    for i in range(C):
        for j in range(R):
            print(mat[j][i].get_bitvector_in_ascii(), end=' ')
    print("\n")    

def convert2DTo1D(mat):
    ret = []
    R = len(mat)
    C = len(mat[0])
    for i in range(C):
        for j in range(R):
            ret.append(mat[j][i])
    return ret

def print1DBitVectorASCII(vec):
    for i in range(len(vec)):
        print(vec[i].get_bitvector_in_ascii(), end='')
    print("\n")

def convertTo1DBitVectorASCII(vec):
    ret = []
    for i in range(len(vec)):
        ret.append(vec[i].get_bitvector_in_ascii())
    return ret
def convertTo1DBitVectorHex(vec):
    ret = []
    for i in range(len(vec)):
        ret.append(vec[i].get_bitvector_in_hex())
    return ret
def decrypt(aesLen,cipherText,allKeys):

    COL = aesLen // 32        # Matrix column

    allKeysRev = allKeys.copy()
    allKeysRev.reverse()

    # add round key
    decrpytic = xor2D(cipherText,allKeysRev[0])
    if DEBUG : 
        print("================================================")
        print("Round 0")
        print2DBitVectorHex(decrpytic)
        print("--------")

    for round in range(1,roundD[aesLen]+1):
        if DEBUG :  
            print("Round ", round)
        decrpytic = subBytes2D(decrpytic,isInv=True)
        decrpytic = rightShift2D(decrpytic)
        decrpytic = xor2D(decrpytic,allKeysRev[round])
        if round != roundD[aesLen]:
            decrpytic = MixColumns(COL,decrpytic,isEncryptMode=False)
        if DEBUG : 
            print2DBitVectorHex(decrpytic)
            print("--------")
    return convert2DTo1D(decrpytic)

def decryptAll(aesLen,cipherTextAra,allKeys):
    ret = []
    for i in range(len(cipherTextAra)):
        ret.extend(decrypt(aesLen,cipherTextAra[i],allKeys))
    return ret

def encrypt(aesLen,text,allKeys):

    COL = aesLen // 32        # Matrix column

    crpytic = convertTo2DHexArray(text)

    # add round key
    crpytic = xor2D(crpytic,allKeys[0])
    if DEBUG : 
        print("================================================")
        print("Round 0")
        print2DBitVectorHex(crpytic)
        print("--------")

    for round in range(1,roundD[aesLen]+1):
        if DEBUG : 
            print("Round ", round)
        crpytic = subBytes2D(crpytic)
        crpytic = leftShift2D(crpytic)
        if round != roundD[aesLen]:
            crpytic = MixColumns(COL,crpytic,isEncryptMode=True)
        crpytic = xor2D(crpytic,allKeys[round])
        if DEBUG : 
            print2DBitVectorHex(crpytic)
            print("--------")

    return crpytic

def encryptAll(aesLen,text,allKeys):
    blockSize = aesLen//8
    textLen = len(text)
    ret = []
    for i in range(0,textLen,blockSize):
        ret.append(encrypt(aesLen,text[i:i+blockSize],allKeys))
    return ret

def printCypherTextHex(crypticAra):
    ret = []
    for i in range(len(crypticAra)):
        cryptic1D = convert2DTo1D(crypticAra[i])
        toAdd = convertTo1DBitVectorHex(cryptic1D)
        toAdd = ''.join(toAdd)
        ret.append(toAdd)
    return ret # Array of hex strings, one element per block
    # retStr = ''.join(ret)
    # print("Hex : ",retStr)
    # return retStr
def reconstruct2DfromHexAll(hexStrAra):
    ret = []
    for i in range(len(hexStrAra)):
        ret.append(reconstruct2DfromHex(hexStrAra[i]))
    return ret

def reconstruct2DfromHex(hexStr):
    # convert hexStr to 1D array
    hex1D = []
    for i in range(0,len(hexStr),2):
        hex1D.append(hexStr[i:i+2])
    # print(hex1D)
    # convert 1D array to 2D array
    hex2D = convertTo2DHexArray(hex1D)
    return hex2D

def printCypherTextASCII(crypticAra):
    ret = []
    for i in range(len(crypticAra)):
        cryptic1D = convert2DTo1D(crypticAra[i])
        ret.append(convertTo1DBitVectorASCII(cryptic1D))
    print("ASCII : ",ret)


def AESEncrypt(aesLen,content,key):
    ## KEY
    start_time = time.time()
    key = processKey(aesLen,key)
    # print("KEY GENERATION STARTED")
    allKeys = generateKey(aesLen,key)
    key_scheduling_time = time.time() - start_time
    # printAllKeys(allKeys)

    start_time = time.time()
    ## TEXT
    text = convertTo1DHexArray(content)

    # insert padding
    blockSize = aesLen//8
    textLen = len(text)
    fillerCount = 0
    while((textLen+fillerCount)%blockSize != 0):
        text.append("00")
        fillerCount += 1

    ## ENCRYPT
    print("ENCRYPTION STARTED")
    crypticAra = encryptAll(aesLen,text,allKeys)
    encryption_time = time.time() - start_time
    hexStrAra = printCypherTextHex(crypticAra)
    return hexStrAra , fillerCount, key_scheduling_time, encryption_time

def AESDecrypt(aesLen,hexStrAra,key,fillerCount):

    ## KEY
    key = processKey(aesLen,key)
    # print("KEY GENERATION STARTED")
    allKeys = generateKey(aesLen,key)

    hex2DAll = reconstruct2DfromHexAll(hexStrAra)
    # print("RECONSTRUCTED HEX : ")
    # print2DBitVectorHex(hex2D)
    # print2DBitVectorHex(crypticAra[0])
    ## DECRYPT
    print("DECRYPTION STARTED")
    decrpytic = decryptAll(aesLen,hex2DAll,allKeys)

    # remove padding
    while fillerCount > 0:
        decrpytic.pop()
        fillerCount -= 1

    return decrpytic
    


def hexToASCII(hexStr):
    binary_str = codecs.decode(hexStr, 'hex')
    return str(binary_str,"ISO-8859-1")  
    
def main():
    key = "BUET CSE17 Batch"
    text = "CanTheyDoTheirFe"
    AES_TYPE = 256
    
    # do aes encryption on text
    hexStrAra, fillerCount, key_scheduling_time, encryption_time =  AESEncrypt(AES_TYPE, text , key)

    # do aes decryption
    start_time = time.time()
    decrpytic = AESDecrypt(AES_TYPE, hexStrAra , key, fillerCount)
    decryption_time = time.time() - start_time

    print("Plain Text : ")
    print(text," [In ASCII]")
    print( ''.join(convertTo1DHexArray(text))," [In Hex]")
    print("")

    print("Key : ")
    print(key," [In ASCII]")
    print( ''.join(convertTo1DHexArray(key))," [In Hex]")
    print("")

    # print("Cipher Text : ")
    # print(''.join(hexStrAra)," [In HEX]")
    # print(hexToASCII(''.join(hexStrAra))," [In ASCII]")
    # print("")

    print("Deciphered Text : ")
    print(''.join(convertTo1DBitVectorHex(decrpytic))," [In HEX]")
    print(''.join(convertTo1DBitVectorASCII(decrpytic))," [In ASCII]")

    print("Execution Time : ")
    print("Key Scheduling Time : ",key_scheduling_time)
    print("Encryption Time : ",encryption_time)
    print("Decryption Time : ",decryption_time)



main()