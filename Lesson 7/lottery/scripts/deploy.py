from brownie import (
    network,
    config,
    Lottery
    )
from scripts.utils import (
    get_account,
    get_contract,
    fund_with_link
    )
import time

ENTRY_FEE=10

def deploy_lottery(entry_fee):
    current_network= network.show_active()
    account = get_account()
    
    print("Current network: "+current_network)

    link_fee=config["networks"][network.show_active()]["fee"]
    key_hash=config["networks"][network.show_active()]["key-hash"]
    eth_usd_price_feed=get_contract("eth_usd_price_feed").address
    vrf_coordinator=get_contract("vrf-coordinator").address
    link_token=get_contract("link-token").address

    print("link_fee: "+str(link_fee==100000000000000000))
    #print("key_hash: "+str(key_hash))
    #print("vrf_coordinator: "+str(vrf_coordinator))
    
    
    print("Deploying Lottery")
    lottey = Lottery.deploy(
        entry_fee,
        eth_usd_price_feed,
        vrf_coordinator,
        link_token,
        link_fee,
        key_hash,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"))
    print("Lottery Deployed")
    return lottey

def start_lottery():
    account=get_account()
    lottery=Lottery[-1]
    starting_tx=lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery has started! run to buy a number!")
    pass

def enter_lottery():
    account=get_account()
    lottery=Lottery[-1]
    value = lottery.getEntranceFee() + 10000000
    enter_tx=lottery.enter({"from": account, "value": value})
    enter_tx.wait(1)
    print(account.address + " entered the lottery :D")
    pass

def end_lottery():
    account=get_account()
    lottery=Lottery[-1]
    #We sent link to the lottery
    fund_tx = fund_with_link(lottery.address)
    fund_tx.wait(1)

    #We end the lottery
    end_tx=lottery.endLottery({"from": account})
    end_tx.wait(1)
    print(account.address + " has ended the lottery :D")
    time.sleep(60)
    print(f"The winner is "+lottery.recentWinner())
    pass


def main():
    deploy_lottery(ENTRY_FEE)
    #start_lottery()
    #enter_lottery()
    #end_lottery()
    pass