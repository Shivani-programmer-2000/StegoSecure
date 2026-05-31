from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import base64, os

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_message_rsa_aes(message, public_key_pem):
    key = os.urandom(16)
    cipher_aes = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode())

    public_key = RSA.import_key(public_key_pem)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(key)

    return base64.b64encode(encrypted_key + cipher_aes.nonce + tag + ciphertext)

def decrypt_message_rsa_aes(data_b64, private_key_pem):
    data = base64.b64decode(data_b64)
    encrypted_key = data[:256]
    nonce = data[256:272]
    tag = data[272:288]
    ciphertext = data[288:]

    private_key = RSA.import_key(private_key_pem)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    key = cipher_rsa.decrypt(encrypted_key)

    cipher_aes = AES.new(key, AES.MODE_EAX, nonce)
    message = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return message.decode()
