import hashlib

def get_sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()
