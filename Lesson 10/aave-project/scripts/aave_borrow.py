from web3 import Web3
from scripts.utils import get_account
from brownie import accounts, interface, config, network

WETH_TO_DEPOSIT=0.02 * (10**18)

def main():
    #getWETH()
    borrow()
    pass

def borrow():
    account = get_account()
    erc20_address=config["networks"][network.show_active()]["weth_token"]
    if(network.show_active() in ["mainnet-fork"]):
        getWETH()
        pass
    lending_pool = get_lending_pool()

    #We need to approve sending our ERC20 tokon
    approve_erc20(WETH_TO_DEPOSIT, lending_pool.address, erc20_address,account)

    # We deposit the WETH
    print("Depositing WETH")
    deposit_tx= lending_pool.deposit(
        erc20_address,
        WETH_TO_DEPOSIT,
        account,
        0,
        {"from": account}
    )
    deposit_tx.wait(1)
    print("WETH deposited")

    # We get data to know how much we can borrow
    borrowable_eth, total_debt=get_borrowable_data(lending_pool,account)

    print("Let's borrow DAI")
    # We want to get DAI, we nned to convert the borrowable ETH to DAI
    dai_eth_price=get_asset_price(config["networks"][network.show_active()]["dai_eth_price_feed"],pair="DAI/ETH")
   
    dai_amount_to_borrow = (borrowable_eth*0.95)/dai_eth_price
    print(f"Dai amount to borrow: {dai_amount_to_borrow}")

    #Now we will borrow
    borrow_tx =lending_pool.borrow(
        config["networks"][network.show_active()]["dai_token"],
        Web3.toWei(dai_amount_to_borrow,"ether"),
        1,
        0,
        account,
        {"from": account}
    )
    borrow_tx.wait(1)
    print("We borrowed some dai")
    get_borrowable_data(lending_pool, account)

    # Repaying
    print("Repaying our loan :'(")
    repay_all(
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
        dai_amount_to_borrow,
        "DAI"
        )
    get_borrowable_data(lending_pool, account)
    pass

def repay_all(lending_pool,asset,account,amount,asset_symbol,rate_mode=1):
    print(f"{account} will repay to {lending_pool.address} the amount of {amount} {asset_symbol}")
    adjusted_amount=Web3.toWei(amount, "ether")
    # First we need to approve the amount of dai to do the repay
    print(f"{account} is approving to transfer {amount} {asset_symbol} to {lending_pool.address}")
    approve_erc20(adjusted_amount,lending_pool.address,asset,account)
    #approve_tx.wait(1)
    print(f"{account} approved to transfer {amount} {asset_symbol} to {lending_pool.address}")
    print(f"{account} is  repaying the amount of {amount} {asset_symbol} to {lending_pool.address}")
    
    repay_tx = lending_pool.repay(
        asset,
        adjusted_amount+1 * (10**1), 
        rate_mode,
        account,
        {"from":account}
    )
    repay_tx.wait(1)
    print(f"{account} repayed the amount of {amount} {asset_symbol} to {lending_pool.address}")
    pass

def get_asset_price(price_feed_address,extra_decimals=0,pair="DAI/ETH"):
    price_feed=interface.AggregatorV3Interface(price_feed_address)
    #print(f"{pair} decimals: {price_feed.decimals()}")
    latest_price=price_feed.latestRoundData()[1]* (10 ** extra_decimals)
    converted_latest_price=Web3.fromWei(latest_price,"ether")
    print(f"Current {pair} price is {converted_latest_price}")
    return float(converted_latest_price)

def get_borrowable_data(lending_pool,account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor
        )=lending_pool.getUserAccountData(account)
    total_collateral_eth= Web3.fromWei(total_collateral_eth,"ether")
    total_debt_eth= Web3.fromWei(total_debt_eth,"ether")
    available_borrow_eth= Web3.fromWei(available_borrow_eth,"ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited")
    print(f"You have {total_debt_eth} worth of ETH borrowed")
    print(f"You can borrow {available_borrow_eth} worth of ETH")
    return(float(available_borrow_eth),float(total_debt_eth))

def approve_erc20(amount, spender, erc20_address, account):
    #The spender will be to who we are going to approve spending our token
    # We need to get the ABI and the address
    print("Approving WETH")
    weth = interface.IERC20(erc20_address)
    approve_tx=weth.approve(spender, amount, {"from": account})
    approve_tx.wait(1)
    print("WETH approved")
    return approve_tx

def get_lending_pool():
    # We need an abi and an address of the lending pool addresses provider
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(config["networks"][network.show_active()]["lending_pool_addresses_provider"])
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    
    # We need an abi and an address of the lending pool
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool

def getWETH():
    """
    Mints WETH by depositing ETH
    """
    # We need to get the ABI and the Address

    # 1. We need to get the account that will interact with the contract
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx =weth.deposit({"from":account, "value": WETH_TO_DEPOSIT})
    tx.wait(1)
    converted_weth=Web3.fromWei(WETH_TO_DEPOSIT,"ether")
    print(f"Received {converted_weth} WETH")
    return tx