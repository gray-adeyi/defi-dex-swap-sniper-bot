from pydantic_settings import BaseSettings, SettingsConfigDict
from eth_typing import Address,ChecksumAddress
from web3.types import ENS

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # Add Your Wallet Address by setting it in the .env file or providing it in your environmental variables
    YOUR_WALLET_ADDRESS: Address|ChecksumAddress|ENS
    # Add Your Private key by setting it in the .env file or providing it in your environmental variables
    YOUR_PRIVATE_KEY: str

    # Add your token address by setting it in the .env file or providing it in your environmental variables
    # Example : "0xc66c8b40e9712708d0b4f27c9775dc934b65f0d9"
    TRADE_TOKEN_ADDRESS: Address|ChecksumAddress|ENS | None = None  # Add token address here example : "0xc66c8b40e9712708d0b4f27c9775dc934b65f0d9"
    WBNB_ADDRESS: Address|ChecksumAddress|ENS = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
    PANCAKE_ROUTER_ADDRESS: Address|ChecksumAddress|ENS = "0x10ED43C718714eb63d5aA57B78B54704E256024E"
    SHOW_TX_ON_BROWSER = True

    SELL_TOKENS = None
    BUY_TOKENS = None

settings = Settings() # type: ignore