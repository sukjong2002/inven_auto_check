import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

BS = 16
pad = lambda s : s+(BS - len(s) % BS) * chr(BS - len(s)%BS).encode()
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def iv():
    return chr(0)*16

class AESCipher(object):
    def __init__(self, key):
        self.key = key

    def encrypt(self, message):
        message = message.encode()
        raw = pad(message)
        cipher = AES.new(self.key.encode("utf8"), AES.MODE_CBC, iv().encode("utf8"))
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode("utf8")

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key.encode("utf8"), AES.MODE_CBC, iv().encode("utf8"))
        dec = cipher.decrypt(enc)
        return unpad(dec).decode("utf8")

#key = '12345678901234567890123456789012'

#message = "test string"
#print(">> message : {}".format(message))

#enc = AESCipher(key).encrypt(message)
#print(">>> enc : {}".format(enc))

#dec = AESCipher(key).decrypt(enc)
#print(">>>dec : {}".format(dec))
