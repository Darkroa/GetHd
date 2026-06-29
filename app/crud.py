from sqlalchemy.orm import Session
from . import models
from .wallet.utils import encrypt_seed
from .wallet.hdwallet import HDWalletManager


def create_master_seed(db: Session, name: str):
    manager = HDWalletManager()

    # 1. Generate a fresh BIP39 mnemonic (shown to user once)
    mnemonic = manager.generate_mnemonic()

    # 2. Derive seed bytes from the mnemonic BEFORE encrypting
    seed_hex = manager.mnemonic_to_seed_hex(mnemonic)

    # 3. Encrypt and store the seed bytes, not the raw mnemonic words
    encrypted = encrypt_seed(seed_hex)

    db_seed = models.MasterSeed(name=name, encrypted_mnemonic=encrypted)
    db.add(db_seed)
    db.commit()
    db.refresh(db_seed)

    # Return mnemonic only here — it is never stored or shown again
    return db_seed, mnemonic


def get_master_seeds(db: Session):
    return db.query(models.MasterSeed).all()


def create_bot_wallet(db: Session, name: str, master_seed_id: int = None):
    wallet = models.BotWallet(name=name, master_seed_id=master_seed_id)
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet
