from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv("local.env")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set")
cipher_suite = Fernet(SECRET_KEY.encode())

def encrypt_mnemonic(mnemonic: str) -> str:
    return cipher_suite.encrypt(mnemonic.encode()).decode()

def decrypt_mnemonic(encrypted: str) -> str:
    try:
        return cipher_suite.decrypt(encrypted.encode()).decode()
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")