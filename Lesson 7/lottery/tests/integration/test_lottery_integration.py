
import pytest
from brownie import network
from scripts.utils import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link)
from scripts.deploy import deploy_lottery
import time

ENTRY_FEE = 5

def test_can_pick_winner_integration():
    print("Correct test")
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        pytest.skip()
    
    account= get_account()
    lottery=deploy_lottery(ENTRY_FEE)
    entry_fee=lottery.getEntranceFee()
    fund_with_link(lottery.address)
    lottery.startLottery({"from": account})

    #There are 3 participants
    lottery.enter({"from": account, "value": entry_fee}).wait(1)
    # lottery.enter({"from": get_account(index=1), "value": entry_fee}).wait(1)
    # lottery.enter({"from": get_account(index=2), "value": entry_fee}).wait(1)

    end_tx = lottery.endLottery({"from": account})
    end_tx.wait(1)
    time.sleep(60)

    winner=lottery.recentWinner()
    lottery_balance= lottery.balance()
    print("Lottery balance: "+str(lottery_balance))
    assert winner == account.address
    assert lottery_balance == 0
    
    pass