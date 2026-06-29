from fastapi import APIRouter, Depends, Form, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import create_master_seed, get_master_seeds, create_bot_wallet
from ..wallet.hdwallet import HDWalletManager
from .auth import get_current_user

router = APIRouter()
manager = HDWalletManager()

@router.post("/master-seed")
def create_seed(name: str = Form(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    seed, mnemonic = create_master_seed(db, name)
    return {"name": name, "mnemonic": mnemonic}  # Show only once

@router.post("/bot-wallet")
def create_bot(
    master_seed_name: str = Form(...),
    bot_name: str = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    seeds = get_master_seeds(db)
    seed = next((s for s in seeds if s.name == master_seed_name), None)
    if not seed:
        raise HTTPException(404, "Master seed not found")

    wallet = create_bot_wallet(db, bot_name, seed.id)
    
    # Background address generation
    background_tasks.add_task(manager.get_addresses_from_db_seed, seed.encrypted_mnemonic)
    
    return {"bot_wallet": wallet}