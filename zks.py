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
os.environ['ZK_SYNC_LIBRARY_PATH'] = 'C:\\Users\\admin\\Downloads\\zks-crypto-windows-x64.dll'
async def zks():
    library = ZkSyncLibrary()
    # Create Zksync Provider
    provider = ZkSyncProviderV01(provider=HttpJsonRPCTransport(network=network.rinkeby))
    # Setup web3 account
    private_key = 'b2f77adac67848ad4b408fcb782d87dd5c574de5dcd93b1361511510f9638189'
    account = Account.from_key(private_key)
    print('账号:',account.address)
    # Create EthereumSigner
    ethereum_signer = EthereumSignerWeb3(account=account)
    # Load contract addresses from server
    contracts = await provider.get_contract_address()
    # Setup web3
    url='https://rinkeby.infura.io/v3/8793b4d684ee466c8240afe0ea75870e'
    w3 = Web3(HTTPProvider(endpoint_uri=url ))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # 注入poa中间件
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
    token = await wallet.resolve_token("ETH")
    # Approve Enough deposit using token contract
    await wallet.ethereum_provider.approve_deposit(token, Decimal(1))

    # Deposit money from contract to our address
    deposit = await wallet.ethereum_provider.deposit(token, Decimal(1),
                                                     account.address)
    print('充值eth：',deposit)

    if not await wallet.is_signing_key_set():
        tx = await wallet.set_signing_key("ETH", eth_auth_data=ChangePubKeyEcdsa())
        status = await tx.await_committed()

    # Committed state is not final yet
    committedETHBalance = await wallet.get_balance("ETH", "committed")

    # Verified state is final
    verifiedETHBalance = await wallet.get_balance("ETH", "verified")
    print('zks账户eth余额:',verifiedETHBalance)
    to_addr = '0x8FF80640B2f57C222510fc85e250e34f946B054B'
    amount = Decimal("0.01")
    print('向%s转账%s'%(to_addr,amount))
    tx = await wallet.transfer(to_addr,amount=amount, token="ETH")
    status = await tx.await_committed()
    print('转账状态：',status)

if __name__ =="__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(zks())
    finally:
        loop.close()