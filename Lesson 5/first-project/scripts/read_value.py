from brownie import accounts, config, SimpleStorage

#Contract[-1] give us the most recent deployment
#Contract[0] give us the first deployment
def read_contract():
    simple_storage=SimpleStorage[-1]
    #Brownie already know the ABI and adress of the contract
    print(simple_storage.retrieve())
    #print(SimpleStorage[0]) #It has the deployed contracts addres

    pass

def main():
    read_contract()
    pass
