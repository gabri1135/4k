from Crypto.Cipher import AES
import hashlib

class Decrypt:
    def __init__(self, key):
        self.decrypt = AES.new(key, AES.MODE_CBC, IV=self.getIV(key))

    def getIV(self, key):
        encoded_str = key.hex().encode()
        hash_obj = hashlib.sha1(encoded_str)
        iv = hash_obj.hexdigest()
        return bytes.fromhex(iv[0:32])

    def get(self, file):
        self.decrypt.decrypt(file)
