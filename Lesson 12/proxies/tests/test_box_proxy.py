from brownie import Contract
from brownie import Box, ProxyAdmin,TransparentUpgradeableProxy
from scripts.utils import get_account,encode_function_data

def test_proxy_delegate_calls():
    account= get_account()
    box = Box.deploy({"from": account})
    proxy_admin=ProxyAdmin.deploy({"from": account})
    box_encoded_initializer_function =encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 10**6}
    )
    
    proxy_box = Contract.from_abi("Box",proxy.address, Box.abi)
    assert proxy_box.retrieve()==0
    proxy_box.store(1, {"from":account})
    assert proxy_box.retrieve()==1
    pass