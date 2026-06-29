from sqlalchemy.orm import Session
from . import models
from .wallet.utils import encrypt_mnemonic

def create_master_seed(db: Session, name: str):
    from .wallet.hdwallet import HDWalletManager
    manager = HDWalletManager()
    mnemonic = manager.generate_mnemonic()
    encrypted = encrypt_mnemonic(mnemonic)
    db_seed = models.MasterSeed(name=name, encrypted_mnemonic=encrypted)
    db.add(db_seed)
    db.commit()
    db.refresh(db_seed)
    return db_seed, mnemonic  # Return plain mnemonic only once

def get_master_seeds(db: Session):
    return db.query(models.MasterSeed).all()

def create_bot_wallet(db: Session, name: str, master_seed_id: int = None):
    wallet = models.BotWallet(name=name, master_seed_id=master_seed_id)
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet