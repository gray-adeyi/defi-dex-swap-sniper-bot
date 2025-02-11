from typing import TypedDict, Unpack,Type
from web3 import Web3
from web3.contract import Contract
from config import settings
import time
from eth_typing import Address,ChecksumAddress
from web3.types import ENS


class BuyTokenOptions(TypedDict):
    symbol: str
    web3: Web3
    wallet_address: Address|ChecksumAddress|ENS
    contract_pancake: Type[Contract] | Contract
    token_to_buy_address: Address|ChecksumAddress|ENS
    wbnb_address: Address|ChecksumAddress|ENS

def buy_tokens(**options: Unpack[BuyTokenOptions]):
    symbol = options.get('symbol')
    web3 = options.get('web3')
    wallet_address = options.get('wallet_address')
    contract_pancake = options.get('contract_pancake')
    token_to_buy_address = options.get('token_to_buy_address')
    wbnb_address = options.get('wbnb_address')

    if not all([symbol,web3,wallet_address,contract_pancake,token_to_buy_address,wbnb_address]):
        raise ValueError('incomplete options provided to buy token. required parameters are `symbol, web3, '
                         'wallet_address, contract_pancake, token_to_buy_address, wbnb_address`')

    to_buy_bnb_amount = input(f"Enter amount of BNB you want to buy {symbol}: ")
    to_buy_bnb_amount = web3.to_wei(to_buy_bnb_amount, 'ether')

    pancake_swap_txn = contract_pancake.functions.swapExactETHForTokens(0,
                                                                      [wbnb_address, token_to_buy_address],
                                                                      wallet_address,
                                                                      (int(time.time() + 10000))).buildTransaction({
        'from': wallet_address,
        'value': to_buy_bnb_amount,  # Amount of BNB
        'gas': 160000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address)
    })

    signed_txn = web3.eth.account.sign_transaction(pancake_swap_txn, private_key=settings.YOUR_PRIVATE_KEY)
    try:
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        result = [web3.to_hex(tx_token), f"Bought {web3.from_wei(to_buy_bnb_amount, 'ether')} BNB of {symbol}"]
        return result
    except ValueError as e:
        if e.args[0].get('message') in 'intrinsic gas too low':
            result = ["Failed", f"ERROR: {e.args[0].get('message')}"]
        else:
            result = ["Failed", f"ERROR: {e.args[0].get('message')} : {e.args[0].get('code')}"]
        return result
