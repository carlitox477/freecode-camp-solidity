from brownie import (
    network,
    config,
    CarlitoxToken
    )

from scripts.utils import (
    get_account,
    )

INITIAL_SUPPLY = 10000 * 10**18

def deploy_token():
    current_network= network.show_active()
    account = get_account()
    
    print("Current network: "+current_network)
    
    print("Deploying carlitox token")
    carli_token = CarlitoxToken.deploy(
        INITIAL_SUPPLY,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"))
    print("Token deployed in "+str(carli_token.address))
    return carli_token


def main():
    deploy_token()
    pass