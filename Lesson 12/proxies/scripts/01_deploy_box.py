from brownie import (
    Contract,
    config,
    network,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    BoxV2
    )
from scripts.utils import get_account, encode_function_data, upgrade, LOCAL_BLOCKCHAIN_ENVIRONMENTS

def deploy_box():
    account = get_account()
    #print(f"Deploying to {network.show_active()}")
    box= Box.deploy({"from": account},publish_source=config["networks"][network.show_active()].get("verify"))
    return box

def deploy_boxV2():
    account = get_account()
    #print(f"Deploying to {network.show_active()}")
    boxV2= BoxV2.deploy({"from": account},publish_source=config["networks"][network.show_active()].get("verify"))
    return boxV2

def deploy_proxy_admin():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    proxy_admin=ProxyAdmin.deploy({"from": account}, publish_source=config["networks"][network.show_active()].get("verify"))
    return proxy_admin

def deploy_proxy(implementation,admin_address, encoded_initializer):
    account = get_account()
    
    #Logic : implementation contract address
    #Admin: Admin address
    #Data: encoded function call
    
    proxy=TransparentUpgradeableProxy.deploy(
        implementation.address, #implementation contract address
        admin_address, #Admin address
        encoded_initializer, #Data: encoded function call
        {"from": account,"gas": 10**6},
        publish_source=config["networks"][network.show_active()].get("verify")
        )
    return proxy

#def main():
#
#    pass

def main():
#def extra():
    #box=deploy_box()
    #boxV2 = deploy_boxV2()
    #proxy_admin=deploy_proxy_admin()
    box=Box[-1]
    boxV2=BoxV2[-1]
    proxy_admin=ProxyAdmin[-1]
    
    print(f"Box value : {box.retrieve()}")
    #initializer=(box.store,1)
    box_encoded_initializer_function=encode_function_data()
    
    print('Deploying proxy')
    proxy = deploy_proxy(box,proxy_admin.address,box_encoded_initializer_function)
    print('Proxy deployed')
    
    #Assign the Box ABI to the proxy address with the box name?
    proxy_box = Contract.from_abi(
        "Box",
        proxy.address,
        Box.abi
        )
    print(f"Box address: {box.address}")
    print(f"Proxy box address: {proxy_box.address}")
    print(f"Proxy address: {proxy.address}")
    proxy_box.store(1,{"from": get_account()})
    print(f"Proxy box retrieve {proxy_box.retrieve()}")
    
    
    upgrade_transcation = upgrade(
        get_account(),
        proxy,
        boxV2.address,
        proxy_admin_contract=proxy_admin
        )
    upgrade_transcation.wait(1)
    print("Proxy has been upgraded")
    proxy_box = Contract.from_abi(
        "BoxV2",
        proxy.address,
        BoxV2.abi
        )
    increment_tx=proxy_box.increment({"from": get_account()})
    increment_tx.wait(1)
    print(f"Proxy box retrieve {proxy_box.retrieve()}")
    pass