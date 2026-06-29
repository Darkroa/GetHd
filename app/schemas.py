from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class MasterSeedCreate(BaseModel):
    name: str

class BotWalletCreate(BaseModel):
    master_seed_name: str
    bot_name: str
    account: int = 0

class AddressResponse(BaseModel):
    btc: List[str]
    eth: List[str]
    usdt: List[str]