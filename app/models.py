from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class MasterSeed(Base):
    __tablename__ = "master_seeds"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    encrypted_mnemonic = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BotWallet(Base):
    __tablename__ = "bot_wallets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    master_seed_id = Column(Integer, ForeignKey("master_seeds.id"), nullable=True)
    btc_address = Column(String, nullable=True)
    eth_address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())