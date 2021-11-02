# from solcx import compile_standard, install_solc
# install_solc("0.6.0")
from solcx import compile_standard
import json
from web3 import Web3
import os 
from dotenv import load_dotenv # To load enviroment variables in .env files

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    pass

# Compile our soliditby code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

#We create a file with all the information about our contract
with open("compiled_code.json","w") as file:
    json.dump(compiled_sol,file)

#We get the bytecide
bytecode= compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
#print(bytecode)

abi= compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
#print(abi)

# To connect to ganache/ a blockchain
node_uri = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(node_uri))
    # We need a provider per instance (new connection to the server)
chain_id = 1337
my_address = os.getenv("PUBLIC_KEY")
private_key = os.getenv("PRIVATE_KEY")

#my_address = "0x3Dc06cb3BBA8EDe0D675b547dAb2159c579fBDCf"
# private_key = "d8d4a6529cd8ff1cf08383f14b75923b61313ac6921f75ffe88b1617ffd6c6cd"
#private_key = os.getenv("ENV_Variable_name")

#Create the contract in python
SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)
#print(SimpleStorage)


#Get the latest transaction from an address
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

#Deploying a transaction
# 1. We need to build a transaction.
transaction = SimpleStorage.constructor().buildTransaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce
})
    # value: ETH we are gona send

# 2. Sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 3. Send a transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_reciept = w3.eth.wait_for_transaction_receipt(tx_hash) #Wait until transaction is don or refused

# To work with a contract we need:
#   * The contract address
#   * The contract ABI
simple_storage= w3.eth.contract(address=tx_reciept.contractAddress, abi = abi)

# Call --> simulate making a call and geting a return value

#print(simple_storage.functions.store(58).call())
#print(simple_storage.functions.retrieve().call())

# Transact --> Make a state change
# 1. We need to build a transaction.
store_nonce = w3.eth.getTransactionCount(my_address)
store_transaction = simple_storage.functions.store(58).buildTransaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": store_nonce
})

# 2. Sign a transaction
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)

# 3. Send a transaction
store_tx_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
#Wait until transaction is don or refused
store_tx_reciept = w3.eth.wait_for_transaction_receipt(store_tx_hash)

print(simple_storage.functions.retrieve().call())



# SimpleStorage.constructor() just invoke the same method that the constructor of the contract
# build transaction requires the transaction parameters in a dictionary
# Both methods are needed to deploy the contract
#print(transaction)
# https://web3py.readthedocs.io/en/stable/contracts.html#methods