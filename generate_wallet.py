#!/usr/bin/env python3
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.wallet.hdwallet import HDWalletManager
from app.crud import create_master_seed, get_master_seeds, create_bot_wallet
from app.wallet.utils import decrypt_mnemonic

manager = HDWalletManager()
db: Session = SessionLocal()

def generate_new_master_seed(name: str):
    mnemonic = manager.get_addresses_from_mnemonic.__self__.__class__()._generate_mnemonic()  # helper
    # Better:
    from bip_utils import Bip39MnemonicGenerator
    mnemonic = str(Bip39MnemonicGenerator().FromWordsNumber(12))
    
    seed_record = create_master_seed(db, name, mnemonic)
    print(f"✅ Master Seed Created: {seed_record.name} (ID: {seed_record.id})")
    print("MNEMONIC (SAVE SECURELY):")
    print(mnemonic)
    return seed_record

def generate_from_existing_seed(seed_name: str, bot_name: str, account=0, num=3):
    seed_record = get_master_seeds(db)  # or filter by name
    for s in seed_record:
        if s.name == seed_name:
            addresses = manager.get_addresses_from_db_seed(s.encrypted_mnemonic, account, num)
            wallet = create_bot_wallet(db, bot_name, s.id)
            
            print(f"\n=== Bot Wallet: {bot_name} ===")
            print(f"Master Seed: {s.name}")
            print("BTC Addresses :", addresses["btc"])
            print("ETH/USDT Addresses :", addresses["eth"])
            return wallet
    print("Seed not found")
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python generate_wallet.py new <seed_name>")
        print("  python generate_wallet.py from <seed_name> <bot_name>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "new" and len(sys.argv) > 2:
        generate_new_master_seed(sys.argv[2])
    elif cmd == "from" and len(sys.argv) > 3:
        generate_from_existing_seed(sys.argv[2], sys.argv[3])
    else:
        print("Invalid command")