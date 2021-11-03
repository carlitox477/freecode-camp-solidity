from brownie import FundMe, accounts, network, config, MockV3Aggregator
from scripts.utils import (get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS)


def deploy_fund_me():
    account = get_account()
    print("Current network: "+network.show_active())

    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        price_feed_address=config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        print("Deploying Mock")
        deploy_mocks()
        price_feed_address=MockV3Aggregator[-1].address
        pass

    print(f"{account} is deploying a FundMe contract")

    fund_me=FundMe.deploy(
        price_feed_address,
        {"from":account},
        publish_source=config["networks"][network.show_active()]["verify"])
    print(f"Contract deployed to {fund_me.address}")
    return fund_me
    pass




def main():
    deploy_fund_me()
    pass

