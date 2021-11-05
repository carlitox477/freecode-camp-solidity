from brownie import (
    network,
    accounts,
    config,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
    interface)

DECIMALS = 8
ETH_STARTING_PRICE_IN_USD = 2000 * 10**8
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development","ganache-testnet-dev"]
FORKED_LOCAL_ENVIROMENTS =['mainnet-fork', 'mainnet-fork-dev']
CONTRACT_TO_MOCK = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf-coordinator": VRFCoordinatorMock,
    "link-token": LinkToken,
}

def get_account(index=None, id=None):
    if(index):
        return accounts[index]
    if(id):
        return accounts.load(id)
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIROMENTS ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    pass

def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.
        Args:
            contract_name (string)
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
    """
    contract_type = CONTRACT_TO_MOCK[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # MockV3Aggregator.abi
    return contract

def deploy_mocks(decimals=DECIMALS, initial_value=ETH_STARTING_PRICE_IN_USD):
    print("Deploying mocks!")
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Mocks Deployed!")

def fund_with_link(contract_address, account=None, link_token=None, amount=1000000000000000000):
    account= account if account else get_account()
    link_token= link_token if link_token else get_contract("link-token")
    
    #opcion 1
    # tx = link_token.transfer(contract_address,amount, {"from":account})
    
    #Opcion 2
    link_token_contract = interface.LinkTokenInterface(link_token.address)

    print("Funding "+contract_address+" with LINK")
    tx = link_token_contract.transfer(contract_address,amount, {"from":account})
    
    link_amount=amount/ (10**18)
    tx.wait(1)

    print(contract_address+": Funded with "+str(link_amount)+" link")
    return tx