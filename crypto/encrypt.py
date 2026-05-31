from Crypto.Cipher import AES
import base64
import hashlib

def encrypt_message(message, key):
    key = hashlib.sha256(key.encode()).digest()
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return base64.b64encode(cipher.nonce + ciphertext).decode()
