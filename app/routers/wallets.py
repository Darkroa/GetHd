from fastapi import APIRouter, Depends, Form, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db, SessionLocal
from ..crud import create_master_seed, get_master_seeds, create_bot_wallet
from .. import models
from ..wallet.hdwallet import HDWalletManager
from .auth import get_current_user

router = APIRouter()
manager = HDWalletManager()


# ── Background task: derive addresses and persist them ──────────────────────

def _derive_and_save(wallet_id: int, encrypted_seed_hex: str):
    """Runs outside the request lifecycle with its own DB session."""
    db: Session = SessionLocal()
    try:
        addresses = manager.get_addresses_from_db_seed(encrypted_seed_hex)
        wallet = db.query(models.BotWallet).filter(models.BotWallet.id == wallet_id).first()
        if wallet:
            wallet.btc_address = addresses["btc"][0]
            wallet.eth_address = addresses["eth"][0]
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"[wallet] address derivation failed for wallet {wallet_id}: {e}")
    finally:
        db.close()


# ── Routes ───────────────────────────────────────────────────────────────────

@router.get("/seeds")
def list_seeds(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_master_seeds(db)


@router.get("/wallets")
def list_wallets(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.BotWallet).all()


@router.post("/master-seed")
def create_seed(
    name: str = Form(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    seed, mnemonic = create_master_seed(db, name)
    return {"name": seed.name, "mnemonic": mnemonic}


@router.post("/bot-wallet")
def create_bot(
    master_seed_name: str = Form(...),
    bot_name: str = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    seeds = get_master_seeds(db)
    seed = next((s for s in seeds if s.name == master_seed_name), None)
    if not seed:
        raise HTTPException(404, "Master seed not found")

    wallet = create_bot_wallet(db, bot_name, seed.id)

    # Derive and persist addresses in the background
    background_tasks.add_task(_derive_and_save, wallet.id, seed.encrypted_mnemonic)

    return {"bot_wallet": {"id": wallet.id, "name": wallet.name}}
