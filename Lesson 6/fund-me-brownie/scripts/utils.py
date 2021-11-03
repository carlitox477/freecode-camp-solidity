from brownie import network, accounts,config,MockV3Aggregator

DECIMALS = 8
ETH_STARTING_PRICE_IN_USD = 2000 * 10**8
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development","ganache-testnet-dev"]
FORKED_LOCAL_ENVIROMENTS =['mainnet-fork', 'mainnet-fork-dev']

def get_account():
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIROMENTS ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    pass

def deploy_mocks():
    print("Deploying mock contract")
    if(len(MockV3Aggregator)<=0):
        MockV3Aggregator.deploy(
            DECIMALS,
            ETH_STARTING_PRICE_IN_USD,
            {"from": get_account()})
        pass
    print("Mock contract deployed")
    pass