from sqladmin import Admin, ModelView
from .database import engine
from .models import MasterSeed, BotWallet


class MasterSeedAdmin(ModelView, model=MasterSeed):
    column_list = ["id", "name", "created_at"]
    can_delete = False


class BotWalletAdmin(ModelView, model=BotWallet):
    column_list = ["id", "name", "btc_address", "eth_address", "created_at"]


def setup_admin(app):
    admin = Admin(app, engine, title="HD Wallet Admin")
    admin.add_view(MasterSeedAdmin)
    admin.add_view(BotWalletAdmin)
    return admin
