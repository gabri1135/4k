from Crypto.Cipher import AES
import hashlib


class Decrypt:
    def __init__(self, key: str) -> None:
        self.decrypt = AES.new(key, AES.MODE_CBC, IV=self.getIV(key))

    def getIV(self, key: str) -> bytes:
        encoded_str = key.hex().encode()
        hash_obj = hashlib.sha1(encoded_str)
        iv = hash_obj.hexdigest()
        return bytes.fromhex(iv[0:32])

    def get(self, file: bytes) -> bytes:
        return self.decrypt.decrypt(file)
