from brownie import Contract
from brownie import Box, ProxyAdmin,TransparentUpgradeableProxy,BoxV2
from scripts.utils import get_account,encode_function_data,upgrade

def test_proxy_delegate_calls():
    account= get_account()
    
    #Deploying contracts
    box = Box.deploy({"from": account})
    proxy_admin=ProxyAdmin.deploy({"from": account})
    boxV2 = BoxV2.deploy({"from": get_account()})
    
    #Encoding box initializer
    box_encoded_initializer_function =encode_function_data()
    #Deploying the proxy
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 10**6}
    )
    
    # creating a contract interface for the proxy
    proxy_box = Contract.from_abi("Box",proxy.address, Box.abi)
    proxy_box.store(1, {"from":account})
    
    #Upgrade transaction
    upgrade_transcation = upgrade(
        account,
        proxy,
        boxV2.address,
        proxy_admin_contract=proxy_admin
        )
    upgrade_transcation.wait(1)
    
    # creating a contract interface for the proxy, we don't initialize nothing here?
    proxy_box = Contract.from_abi(
        "BoxV2",
        proxy.address,
        BoxV2.abi
        )
    increment_tx=proxy_box.increment({"from": account})
    increment_tx.wait(1)
    
    assert proxy_box.retrieve()==2
    pass