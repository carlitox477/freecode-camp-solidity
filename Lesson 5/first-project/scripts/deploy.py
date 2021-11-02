from brownie import accounts, config, SimpleStorage, network

def deploy_simple_storage():
    account = get_account()
    #print(account)
    
    simple_storage = SimpleStorage.deploy({
        "from": account,
    }) # It return an object that represent the contract

    #We can call functions inmediatelly
    stored_value = simple_storage.retrieve() 
    print(stored_value)

    transaction = simple_storage.store(58, {"from": account})
    transaction.wait(1)
    print(simple_storage.retrieve())
    #account=accounts.add(config["wallets"]["from_key"])
    #print(account)
    pass

def get_account():
    if(network.show_active()=="development"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    pass

def main():
    #print("hello")
    deploy_simple_storage()
    pass
