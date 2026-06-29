from bip_utils import (
    Bip39SeedGenerator,
    Bip39MnemonicGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes,
    EthAddr,
)
from .utils import decrypt_seed


class HDWalletManager:
    def generate_mnemonic(self) -> str:
        return str(Bip39MnemonicGenerator().FromWordsNumber(12))

    def mnemonic_to_seed_hex(self, mnemonic: str) -> str:
        """Derive the BIP39 seed bytes from a mnemonic and return as hex."""
        return Bip39SeedGenerator(mnemonic).Generate().hex()

    def get_addresses_from_seed_hex(
        self, seed_hex: str, account: int = 0, num: int = 5
    ) -> dict:
        """Derive BTC / ETH addresses directly from raw seed bytes (hex)."""
        seed_bytes = bytes.fromhex(seed_hex)

        # Bitcoin
        btc_wallet = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        btc_ext = (
            btc_wallet.Purpose().Coin().Account(account).Change(Bip44Changes.CHAIN_EXT)
        )
        btc_addrs = [btc_ext.AddressIndex(i).PublicKey().ToAddress() for i in range(num)]

        # Ethereum + USDT (same address space)
        eth_wallet = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
        eth_ext = (
            eth_wallet.Purpose().Coin().Account(account).Change(Bip44Changes.CHAIN_EXT)
        )
        eth_addrs = [
            EthAddr.EncodeKey(eth_ext.AddressIndex(i).PrivateKey().Raw().ToHex())
            for i in range(num)
        ]

        return {"btc": btc_addrs, "eth": eth_addrs, "usdt": eth_addrs}

    def get_addresses_from_mnemonic(
        self, mnemonic: str, account: int = 0, num: int = 5
    ) -> dict:
        """Convenience: derive from a plain mnemonic."""
        seed_hex = self.mnemonic_to_seed_hex(mnemonic)
        return self.get_addresses_from_seed_hex(seed_hex, account, num)

    def get_addresses_from_db_seed(
        self, encrypted_seed_hex: str, account: int = 0, num: int = 5
    ) -> dict:
        """Decrypt the stored seed hex and derive addresses."""
        seed_hex = decrypt_seed(encrypted_seed_hex)
        return self.get_addresses_from_seed_hex(seed_hex, account, num)
