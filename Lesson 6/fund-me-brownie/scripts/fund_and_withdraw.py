from brownie import FundMe
from scripts.utils import get_account

def fund():
    account = get_account()
    fund_me =FundMe[-1]
    entrance_fee= fund_me.getEntranceFee()
    print(f"The current entry fee is {entrance_fee} WEI")
    print("Funding")
    fund_me.fund({"from": account, "value": entrance_fee})
    #print(entrance_fee)
    pass

def withraw():
    account = get_account()
    fund_me =FundMe[-1]
    fund_me.withdraw({"from": account})

def main():
    fund()
    withraw()
    pass