# pip install pycryptodome,pyzipper

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64
import os
import pyzipper

def enc(plaintext: str, password: str) -> str:
    iv = os.urandom(16)
    key = PBKDF2(password,iv,dkLen=32,count=100000)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    combined = iv + ciphertext
    return base64.b64encode(combined).decode('utf-8')

def dec(encrypted_data: str, password: str) -> str:
    combined = base64.b64decode(encrypted_data)
    iv = combined[:16]
    ciphertext = combined[16:]
    key = PBKDF2(password,iv,dkLen=32,count=100000)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode('utf-8')

def enczip(filetxt: str, password: str) -> bytes:    
    with open('file.txt','w') as txtf:
        txtf.write(filetxt)
    with pyzipper.AESZipFile('file.zip','w',compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(password.encode('utf-8'))
        zf.write('file.txt')
    zipdata = ''
    with open('file.zip','rb') as bzipf:
        return bzipf.read()
    return zipdata
        
