import json
from pathlib import Path

import sandbox
from web3 import Web3


def deploy(
    web3: Web3, deployer_address: str, deployer_private_key: str, player_address: str
) -> str:
    contract_info = json.loads(Path("compiled/Setup.sol/Setup.json").read_text())
    contract = web3.eth.contract(
        abi=contract_info["abi"], bytecode=contract_info["bytecode"]["object"]
    )
    transaction = contract.constructor().build_transaction(
        {
            "from": deployer_address,
            "nonce": web3.eth.get_transaction_count(deployer_address),
            "value": Web3.to_wei(100, "ether"),
        }
    )
    signed = web3.eth.account.sign_transaction(transaction, deployer_private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

    return receipt.contractAddress


app = sandbox.run_launcher(deploy)
