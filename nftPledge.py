## 监控合约中的nft
## 整理为  addr: [tokenid, tokenid]

from web3 import Web3

import json, time
from web3.middleware import geth_poa_middleware
# contractAddress = "0xE1448DA8eA889c65604a950126A4ffD27CC2a37a"
# contractAddress = "0x07803F6e474d2f4AedF942AF30E5597c8c01921B"
# wallet_address = "0x63d3433c68744A14b243d1fc880ED52eB2C9b7fA"
# wallet_private_key = "e2084389b02f02f032f61979233220077245c343be8c1a565a355cbdbe1fb2b9"
contractAddress = Web3.toChecksumAddress("0xb0ad37b39727845ced84b8628add757f665c0fc2")
wallet_address = Web3.toChecksumAddress("0x02c5Bd57CD3B5122d05ad6212d9498321a42f2Aa")
wallet_private_key = "b2f77adac67848ad4b408fcb782d87dd5c574de5dcd93b1361511510f9638189"

abi = [{
    "inputs": [],
    "name": "distribution",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
}, {
    "inputs": [
        {
            "internalType": "address",
            "name": "account",
            "type": "address"
        }
    ],
    "name": "isexits",
    "outputs": [
        {
            "internalType": "bool",
            "name": "",
            "type": "bool"
        }
    ],
    "stateMutability": "view",
    "type": "function",
    "constant": True
}, {
    "inputs": [],
    "name": "signup",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
}, ]
# with open("bnb_abi.json","r") as f:
#     abi = json.load(f)
#     print("加载abi文件完成...")
print(abi)

# infura_url = "https://bsc-dataseed1.binance.org/"
infura_url = "https://data-seed-prebsc-1-s1.binance.org:8545"

w3 = Web3(Web3.HTTPProvider(infura_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # 注入poa中间件
nft_contract = w3.eth.contract(
    address=contractAddress,
    abi=abi
)


# w3.eth.enable_unaudited_features()

# account = web3.eth.account.from_key("你的私钥")

# web3 = Web3(Web3.HTTPProvider("RPC节点"))
# tx = {
# 'from': account.address,
#     'to': "目标地址",
#     'nonce': web3.eth.getTransactionCount(account),
#     'value': web3.toWei(1, 'ether'),
#     'gas': 2000000,
#     'gasPrice': web3.toWei('5', 'gwei')
# }
# signed = account.signTransaction(tx)
# web3.eth.sendRawTransaction(signed.rawTransaction)

def broadcast_an_opinion(contract):
    nonce = w3.eth.getTransactionCount(wallet_address)
    print("nonce:{}".format(nonce))
    # txn_dict = contract.functions.broadcastOpinion(covfefe).buildTransaction({
    txn_dict = contract.functions.distribution().buildTransaction({
        # 'chainId': 56,
        'chainId': 97,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.toWei('40', 'gwei'),
    })
    print("txn_dict:{}".format(txn_dict))

    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)
    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print("result:{}".format(result))
    tx_receipt = w3.eth.getTransactionReceipt(result)


    count = 0
    while tx_receipt is None and (count < 30):
        time.sleep(10)
        tx_receipt = w3.eth.getTransactionReceipt(result)
        print(tx_receipt)

    if tx_receipt is None or tx_receipt == False:
        return {'status': 'failed', "result": result, 'error': tx_receipt}
    return {'status': 'success', "result": result}


if __name__ == "__main__":
    # 获取nft总数
    number = nft_contract.functions.isexits("0xD1E01D5A8483e1a7e4A2AF1F5F6B66B1FC6D8507").call()
    print(number)
    print(nft_contract.all_functions())
    print(broadcast_an_opinion(nft_contract))