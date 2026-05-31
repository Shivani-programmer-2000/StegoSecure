from Crypto.Cipher import AES
import base64
import hashlib

def decrypt_message(encrypted_text, key):
    try:
        key = hashlib.sha256(key.encode()).digest()
        encrypted = base64.b64decode(encrypted_text)
        nonce = encrypted[:16]
        ciphertext = encrypted[16:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt(ciphertext).decode()
    except:
        return "[Decryption Failed]"
