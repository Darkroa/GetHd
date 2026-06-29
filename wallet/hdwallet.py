from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, EthAddr, Bip39MnemonicGenerator
from .utils import decrypt_mnemonic

class HDWalletManager:
    def generate_mnemonic(self) -> str:
        return str(Bip39MnemonicGenerator().FromWordsNumber(12))

    def get_addresses_from_mnemonic(self, mnemonic: str, account: int = 0, num: int = 5):
        seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
        results = {}

        # Bitcoin
        btc_wallet = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        btc_ext = btc_wallet.Purpose().Coin().Account(account).Change(Bip44Changes.CHAIN_EXT)
        results["btc"] = [btc_ext.AddressIndex(i).PublicKey().ToAddress() for i in range(num)]

        # Ethereum + USDT
        eth_wallet = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
        eth_ext = eth_wallet.Purpose().Coin().Account(account).Change(Bip44Changes.CHAIN_EXT)
        eth_addrs = [EthAddr.EncodeKey(eth_ext.AddressIndex(i).PrivateKey().Raw().ToHex()) for i in range(num)]
        results["eth"] = eth_addrs
        results["usdt"] = eth_addrs

        return results

    def get_addresses_from_db_seed(self, encrypted_mnemonic: str, account: int = 0, num: int = 5):
        mnemonic = decrypt_mnemonic(encrypted_mnemonic)
        return self.get_addresses_from_mnemonic(mnemonic, account, num)