from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv("local.env")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set")
cipher_suite = Fernet(SECRET_KEY.encode())


def encrypt_seed(seed_hex: str) -> str:
    """Encrypt a hex-encoded seed for storage."""
    return cipher_suite.encrypt(seed_hex.encode()).decode()


def decrypt_seed(encrypted: str) -> str:
    """Decrypt stored seed back to hex string."""
    try:
        return cipher_suite.decrypt(encrypted.encode()).decode()
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")


# Legacy aliases kept for any existing callers
def encrypt_mnemonic(data: str) -> str:
    return encrypt_seed(data)


def decrypt_mnemonic(data: str) -> str:
    return decrypt_seed(data)
