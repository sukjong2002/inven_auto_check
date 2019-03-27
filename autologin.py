import pycryptodome
import os
import sys

def check(key, loc, state):
    file = os.path.isfile(loc)
    if state == 'getid':
        if file == True:
            f = open(loc, 'rb')
            userid = f.readline().decode()
            f.close()
            pi = pycryptodome
            decid = pi.AESCipher(key).decrypt(userid)
            return decid

    elif state == 'getpass':
        if file == True:
            f = open(loc, 'rb')
            f.readline().decode()
            password = f.readline().decode()
            f.close()
            pi = pycryptodome
            decpass = pi.AESCipher(key).decrypt(password)
            return decpass

    elif state == 'getkey':
        if file == True:
            f = open(loc, 'rb')
            f.readline().decode()
            f.readline().decode()
            message = f.readline().decode()
            f.close()
            pi = pycryptodome
            decmes = pi.AESCipher(key).decrypt(message)
            if(decmes == 'true'):
                return True
    else:
        return False
