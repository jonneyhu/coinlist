import asyncio
from decimal import Decimal

from eth_account import Account
from web3 import Web3, HTTPProvider
from zksync_sdk import ZkSyncLibrary, ZkSyncProviderV01, HttpJsonRPCTransport, network, EthereumSignerWeb3, ZkSync, \
    EthereumProvider, ZkSyncSigner, Wallet
import os
# Load crypto library
from web3.middleware import geth_poa_middleware
from zksync_sdk.types import ChangePubKeyEcdsa

# os.environ['ZK_SYNC_LIBRARY_PATH'] = 'C:\\Users\\admin\\Downloads\\zks-crypto-windows-x64.dll'
os.environ['ZK_SYNC_LIBRARY_PATH'] = '/home/jonney/Downloads/zks-crypto-linux-x64.so'


def create_aaacount():
    account = Account.create('zksync airdrop')
    print('创建账号', account.address, account.key.hex())
    with open('zks_airdrop.txt', 'a') as w:
        w.write('{} {}\r'.format(account.address, account.key.hex()))
    return account


async def transfer(source_key, target_addr, amount=0):
    library = ZkSyncLibrary()
    # Create Zksync Provider
    provider = ZkSyncProviderV01(provider=HttpJsonRPCTransport(network=network.mainnet))
    # Load contract addresses from server
    contracts = await provider.get_contract_address()
    # Setup web3
    url = 'https://mainnet.infura.io/v3/8793b4d684ee466c8240afe0ea75870e'
    w3 = Web3(HTTPProvider(endpoint_uri=url))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # 注入poa中间件
    account = Account.from_key(source_key)
    # account = create_account()
    # Create EthereumSigner
    ethereum_signer = EthereumSignerWeb3(account=account)
    # Setup zksync contract interactor
    zksync = ZkSync(account=account, web3=w3,
                    zksync_contract_address=contracts.main_contract)
    # Create ethereum provider for interacting with ethereum node
    ethereum_provider = EthereumProvider(w3, zksync)

    # Initialize zksync signer, all creating options were described earlier
    signer = ZkSyncSigner.from_account(account, library, network.rinkeby.chain_id)
    # Initialize Wallet
    wallet = Wallet(ethereum_provider=ethereum_provider, zk_signer=signer,
                    eth_signer=ethereum_signer, provider=provider)

    # Find token for depositing
    # token = await wallet.resolve_token("ETH")
    # Approve Enough deposit using token contract
    # await wallet.ethereum_provider.approve_deposit(token, Decimal(1))

    # Deposit money from contract to our address
    # deposit = await wallet.ethereum_provider.deposit(token, Decimal(1),
    #                                                  account.address)
    # print('充值eth成功交易地址：',deposit.blockHash.decode())

    # if not await wallet.is_signing_key_set():
    #     tx = await wallet.set_signing_key("ETH", eth_auth_data=ChangePubKeyEcdsa())
    #     status = await tx.await_committed()
    #     print('changepubkey status:', status.status)
    # Committed state is not final yet

    # Verified state is final
    verifiedETHBalance = await wallet.get_balance("ETH", "verified")
    print('verified balance:', verifiedETHBalance / pow(10, 18))
    while 1:
        committedETHBalance = await wallet.get_balance("ETH", "committed")
        print('committed balance:', committedETHBalance / pow(10, 18))
        if committedETHBalance > 0.001:
            break
    print('{}zks账户eth余额:{}'.format(account.address, verifiedETHBalance / pow(10, 18)))
    to_addr = target_addr
    if amount == 0:
        amount = (committedETHBalance - 0.00045 * pow(10, 18)) / pow(10, 18)
        amount = Decimal("%s" % amount)
    else:
        amount = Decimal("%s" % amount)
    # amount = Decimal("%s"%(verifiedETHBalance/pow(10,18)))
    print('%s向%s 转账 %s' % (account.address, to_addr, amount))
    tx = await wallet.transfer(to_addr, amount=amount, token="ETH")
    status = await tx.await_committed()
    print('转账状态：', status.status)


async def zks():
    with open('zks_airdrop.txt')as r:
        addresses = r.readlines()
    # private_key = '0xb2f77adac67848ad4b408fcb782d87dd5c574de5dcd93b1361511510f9638189'
    # await transfer(private_key,addresses[0].strip().split(' ')[0],0)
    for i in range(42, len(addresses)):
        if i == len(addresses):
            source = addresses[-1].strip().split(' ')
            target = addresses[0].strip().split(' ')
        else:
            source = addresses[i].strip().split(' ')
            target = addresses[i + 1].strip().split(' ')
        private_key = source[1]
        target_addr = target[0]
        try:
            await transfer(private_key, target_addr)
        except Exception as e:
            print(i)
            raise e


async def activate(source_key):
    library = ZkSyncLibrary()
    # Create Zksync Provider
    provider = ZkSyncProviderV01(provider=HttpJsonRPCTransport(network=network.mainnet))
    # Load contract addresses from server
    contracts = await provider.get_contract_address()
    # Setup web3
    url = 'https://mainnet.infura.io/v3/8793b4d684ee466c8240afe0ea75870e'
    w3 = Web3(HTTPProvider(endpoint_uri=url))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # 注入poa中间件
    account = Account.from_key(source_key)
    # account = create_account()
    # Create EthereumSigner
    ethereum_signer = EthereumSignerWeb3(account=account)
    # Setup zksync contract interactor
    zksync = ZkSync(account=account, web3=w3,
                    zksync_contract_address=contracts.main_contract)
    # Create ethereum provider for interacting with ethereum node
    ethereum_provider = EthereumProvider(w3, zksync)

    # Initialize zksync signer, all creating options were described earlier
    signer = ZkSyncSigner.from_account(account, library, network.rinkeby.chain_id)
    # Initialize Wallet
    wallet = Wallet(ethereum_provider=ethereum_provider, zk_signer=signer,
                    eth_signer=ethereum_signer, provider=provider)

    if not await wallet.is_signing_key_set():
        tx = await wallet.set_signing_key("ETH", eth_auth_data=ChangePubKeyEcdsa())
        status = await tx.await_committed()
        print('changepubkey status:', status.status)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(transfer('0x9ca5895c0da27df434bf288585b7cbafa57397d102c2bb044daf8dc4d254885e','0xa4C19E838e3Aaa80F1F6F87b327544EBAa18ce77'))
    finally:
        loop.close()
    # for i in range(500):
    #     create_aaacount()
