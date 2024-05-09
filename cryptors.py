import pprp
import base64

password = "peekabeyoufoundme"

def xor(block, iv):
    result = [(a ^ b) for (a, b) in zip(block, iv)]
    return bytes(result)

def printbytes(name, array):
    print(name, ", ".join([str(i) for i in array]))

# Rijndael 256 with CBC (iv + salt) decryption
def CBC_decrypt(key, s, iv, block_size=32):
    r = pprp.crypto_3.rijndael(key, block_size=block_size)

    i = 0
    for block in s:
        decrypted = r.decrypt(block)
        decrypted = xor(decrypted, iv)  
        iv = block

        yield decrypted
        i += 1

def decrypt(cipher):
    array = list(bytearray(base64.b64decode(cipher)))
    salt = array[:32]
    rgbIV = array[32:64]
    array2 = array[64:]
    kbytes = pprp.pbkdf2(password.encode('utf-8'), bytes(salt), 32, iterations=1000)

    blocksize = 32
    sg = pprp.data_source_gen(array2, blocksize)
    dg = CBC_decrypt(kbytes, sg, rgbIV, blocksize);
    decrypted = pprp.decrypt_sink(dg, blocksize).decode("utf-8")
    
    return decrypted

# Rijndael 256 with CBC (iv + salt) encryption
def CBC_encrypt(key, s, iv, block_size=32):
    r = pprp.crypto_3.rijndael(key, block_size=block_size)

    i = 0
    for block in s:
        len_ = len(block)
        if len_ < block_size:
            padding_size = block_size - len_
            block += (chr(padding_size) * padding_size).encode('ASCII')
        
        xored = xor(block, iv)
        encrypted = r.encrypt(xored)
        iv = encrypted

        yield encrypted
        i += 1

def encrypt(plaintext):
    joke = "MADE/BY/CATALYST/42/"
    joke = bytes(base64.b64decode(joke))

    salt = joke + bytes([0]*(32 - len(joke)))
    rgbIV = bytes([0]*32)
    array2 = list(bytes(plaintext.encode("utf-8")))
    kbytes = pprp.pbkdf2(password.encode('utf-8'), bytes(salt), 32, iterations=1000)

    blocksize = 32
    sg = pprp.data_source_gen(array2, blocksize)
    dg = CBC_encrypt(kbytes, sg, rgbIV, blocksize)
    encrypted = pprp.encrypt_sink(dg)
    encrypted = base64.b64encode(salt + rgbIV + encrypted)
    
    return encrypted
