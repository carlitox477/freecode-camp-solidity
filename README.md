# Introduction
Notes from the [freecodcamp blockchain course](https://www.youtube.com/watch?v=M576WGiDBdQ)
The only prequesite is having basic python, js, html, and css knowledge.

# Lesson 0
I won't give details about the Lesson 0 part because I already knew the concepts
* Oracles: allow us to interact with off-chain data
* Hybrid smart contracts combine on-chain and off-chain components
* Bitcoin is like digital gold
* Ethereum allows for smart contracts
* Chainlink provides data and external computation to smart contracts

## Blockchain and smart contracts advantages
1. Decentralization: There is no centralize control. No state or central entity can regulate them. Only nodes that support the blockchain can affect its decisions
1. Transparency & flexibility: Everything done here can be seen by everyone.
1. Speed and efficiency: Financial transactions are done almost inmediately.
1. Security and immutability: Data and programs can't be modified. As long as one node is running, data will stay. Hacking a blockchain is almost imposible and harder than hacking a centralize entity.
1. Removal of counterparty risk: Instead of trusting in a person, we trust in maths and criptography.
1. Trust minimized agreements: Smart contracts always acts the same way

## Gas Concepts
* Gas is a unit of computational measure. The more computation a transaction uses the more "gas" you have to pay for. Every transaction that happens on-chain pays a "gas fee" to node operators".
* Gas price: How much it costs per unit of gas. It is usually measured in GWEI
* Gas limit: Max amount of gas in a transaction
* Transaction fee: Gas used * gas price.

Gas price is based off the "demand" of the blockchain. The more people want to make transactions, the higher the gas price, and therefore the higher the transaction fees.

# Lesson 1
* The first thing we need to do when we create a solidity program is defining the solidity compiler version.
```solidity
pragma solidity ^0.6.0; //We use solidity 0.6.0
pragma solidity >=0.6.0; //We use a solidity version greater than or equal to 0.6.0
pragma solidity <=0.6.0 //We use a solidity version lower than or equal to 0.6.0;
pragma solidity >=0.6.0 <=0.9.0; //We use a solidity version greater than or equal to 0.6.0 and lower than or equal to 0.9.0
```
* A contract is similar to a class in other languages. To define a contract:
```solidity
contract Contract{
    //code
}
```
Functions visibility:
* external: it can be called only by other contracts
* public: can be call by everyone
* internal: Default visibility. Can be only called by functions in the current contract or contracts derivering from it (similar to protected in java)
* private: Can only be called by funtions in the current contract

## Function types
* view: To just read data from the blockchain. They doesn't require gas to be executed. It is just for queries
* pure: They don't store data in the blockchain or query data from the contract. They may do operation inside though

```solidity
function retrieve() public view returns(uint256){
    return 1;
}

function sum(uinit256 num1, uinit256 num2) public pure returns(uint256){
    return num1 + num2;
}
```

State-changing function calls are called transactions

## Structs
They allow us to define new types in solidity. Is like defining a typed json.
```solidity
struct People {
    string name;
    uint256 age;
}
```
## Arrays
An array is a way of storing a list of an object or type. To add an element to an array we can use the function ```push```

Variables types in functions:
* memory: Data will only be stored during the execution of the function
* storage: data will persist after execution

## Mapping
A dictionary like data structure, with one value per key
```solidity
//Declaration example
mapping(string => uint256) public nameToAge

//Writing example
nameToAge["Charlie"]=27
```

## How deploy a contract using metamask and remix?
1. Make a contract
1. Install metamask and connect to the mainet/testnet where you want to deploy the contract.
1. Use remix, and in deploy enviroment chose "Injected Web3". Also "Web3 provider" can b euse if we want to use our own node?


# Lesson 2: Factory pattern
A factory contract is a contrac that allow us to generate another contract.
* How do we import a contract?
```solidity
import "contract/path/contract.sol"
```
* Herence:
```solidity
contract Son is Father{
    //....
}
```

# Lesson 3
Key values:
* ```msg.sender```: The address which call the function
* ```msg.value```: Value in wei send with the function
* *payable*: allows a function be call with wei
* ABI (Application Binary interface): tells solidity and other programming languages how it can itneract with other contract.
* *Using* keyord: The directive ```using A for B``` can be used to attach library functions (from the library A) to any type (B) in the context of the contract.
* About SafeMath:
    * For versions >=0.8.0 we don't need it anymore;
    * For versions >=0.6.6 we don't need to call it explicitly;


# Financial decisions
* Invest in cryptos. If it hasn't explode yet it main launchpad and dex are good options too.
* Decentralization gives value to a blockchain

# Lesson 4
We need to install python, pip and py-solc-x before starting to work.
* [python installation](https://www.python.org/downloads/)
* [pip installation](https://phoenixnap.com/kb/install-pip-windows)
* [py-solc-x](https://pypi.org/project/py-solc-x/)

We may have problems with the PATH on windows if we are working in VSC, probabbly a wrong path for python executable. More information [here](https://geek-university.com/python/add-python-to-the-windows-path/)

## Reaading our first smart contract from a file
First we need to install a compiler, so we need to execute a file with the next lines of code
```python
from solcx import install_solc
install_solc("0.6.0")
```

Then, in the file where most of our functionalitites will be developed we need to:
1. Import the compiler
1. Read the file with our contract
1. Compile our solidity code

```python
# Import the compiler
from solcx import compile_standard

#Read the file with our contract
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    pass

# Compile our solidity code
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

```

The ABI is a JSON file which content a description of all the functions of the contract.

To interact with any blockchain we need to use the library web3 and create a web3 provider
```python
from web3 import Web3

node_uri = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(node_uri)) #We need a provider per instance
```

To deploy a contract we need to
1. Build a transaction.
1. Sign a transaction
1. Send a transaction

For this we need to code:
```python

# First we get the ABI and the bytecode
bytecode= compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi= compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#Then we create the contract in python (it gives a special python object)
SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode) 

# We build the transaction
transaction = SimpleStorage.constructor().buildTransaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce
})

# 2. We sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 3. Send a transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# We can wait until transaction is done or refused to continue
tx_reciept = w3.eth.wait_for_transaction_receipt(tx_hash) 
```

## Working with a contract
To interact with a deployed contract we need a provider, a contact address and an ABI

``` python
simple_storage= w3.eth.contract(address=tx_reciept.contractAddress, abi = abi)
```

We can interact with a contract in 2 ways:
* Using the call function, which simulates doing a calling to a function (so, we don't spend gas)
* Using the transact function, which do a call to the blockchain (we spend gas)

In any of this cases we need to access to the functions object of the contract, call the ABI function (it return an object, it doesn't call the function) and decide if we want to use the *call* or the *transact* function.

```python
simple_storage.functions.retrieve().call()
```

Transaction with a contract is pretty similar to deploy it
```python
# 1. We need to build a transaction.
#First we get a new nonce
store_nonce = w3.eth.getTransactionCount(my_address)

# We use the specif instance of the contract we got before. we need to access to the atribute functions and after that decide whiche ABI function use (and send the parameters here of cars)

pre_build_store_transaction= simple_storage.functions.store(58)

# We build the transaction
store_transaction = pre_build_store_transaction.buildTransaction({
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

#Continue
```

## Web 3 instalation
We may need to install first cytoolz with ```pip install cython```
Then we can isntal Web3 with ```pip install web3```

To use variables in .env files we will need to instal the package **python-dotenv**

## Ganache-cli in console
To use ganache in the console
[Documentation](https://www.npmjs.com/package/ganache-cli)

# Lesson 5: Brownie
Brownie is a Python-based development and testing framework for smart contracts targeting the Ethereum Virtual Machine.

To install it we can use:
1. ```python3 -m pip install --user pipx```
1. ```python3 -m pipx ensurepath```
1. ```pipx install eth-brownie```

Or just: 
1. ```pip install --user pipx```
1. ```pipx ensurepath```
1. ```pip install eth-brownie```

To init a project just use the line: ```brownie init project-name```
This will create the next folders:
* build: Track down level information
    * contracts: compiled contract
    * deployments: Across all different chains
    * interfaces
* contracts: Contracts in solidity
* interfaces
* reports
* scripts: To automate tasks
* tests

To compile our code we need to be in the main folder and run ```brownie compile```

To interact with a mainet or testnet we need to add a new account. We can do this with the command:
```brownie accounts new <account-alias>```

This will request a private key that will be cypher, an a generic password. This will hide the private key in our computer.

To delete any of the accounts information we can run ```brownie accounts delete <account-alias>```.

To list all the accounts saved we can run ```brownie accounts list```

## brownie-config.yaml
A special file to configure brownie behaviour
[Documentation](https://eth-brownie.readthedocs.io/en/stable/config.html)

## Deploy a contract
To deploy the contract we need to import it into the deploy file and use the function deploy which just require an account from where deploy
```python
from brownie import SimpleStorage
simple_storage = SimpleStorage.deploy({"from": account})

# To transact we need to specified from what address we are interacting (and brownie should know t private key)
transaction = simple_storage.store(58, {"from": account}) 

# To wait 1 block
transaction.wait(1)

# To get the new value
print(simple_storage.retrieve())
```

## Interacting with contract
We can write otrhe script to itneract with the contract. It is important to run it like ```brownie run scripts/new-script.py --network networkname``` if it is a mainet/testnet

We need to import the contract we want to use from brownie, this will bring all its deployment, which we can access as if they where in an array. For instance:
```python
brownie import Contract
Contract[-1] #give us the most recent deployment
Contract[0] #give us the first deployment
```

## Brownie console
We need to execute the line ```brownie console```

## Testing
A test should be writen in python, put in the test folder, and its code should have functions with the next structure:
1. Arrange: Preliminary data to do the test, and the expected value
1. Act: A contract call or transaction with the arrange data
1. Assert: Where we check the value obtained with the value expected
For instance: 
```python
def test_deploy():
    # Arrange
    account = accounts[0]
    expected = 15
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    
    # Assert
    assert starting_value ==expected
    pass
```

To run:
* Every test: ```brownie test```
* A particular test: ```brownie test -k test_function_name```
* Every test and show variables when everything fails: ```brownie test --pdb```
* It will specified which test went ok and which one no: ```brownie test -s```

The ```brownie test``` depends on pytest, so we can look to [pytest documentaction](https://docs.pytest.org/en/6.2.x/getting-started.html) to learn more about testing

# Lesson 6
## Importing chainlink contracts
While Remix understand that **@chailink/contracts** reffers to chailinks contracts that can be download by npm, brownie doesn't. However, brownie CAN download them from github. The problemas relays on, that if we upload this contract to the blockchain with github references, this may not work (the repository can be  changed), but we can tell brownie to change **@chailink/contracts** with other string when it run it. This can be done in our *brownie-config.yaml*. For instance
```yaml
dependencies:
  #- <organization/repo>@<version>
  - smartcontractkit/chainlink-brownie-contracts@1.1.1
compiler:
  solc:
    remappings:
      - '@chainlink=smartcontractkit/chainlink-brownie-contracts@1.1.1'
```

## Verify contracts
We will need to delete the imported code and add its code. Replacing immports with the actual code is known as "flattening".

A better way to verify the contract is take advantage of brownie deploy function. With an etherscan API key we can verify our contract inmediatelly after deploying with the next code:
```python
account = get_account()
contract=Contract.deploy({"from":account}, publish_source=True)
```
This will require to specify in the .env file the etherscan token as:
```
export ETHERSCAN_TOKEN = <API-KEY>
```

## Mock contracts
A mok contract is one which is deployed on our develompent network to simulate a contract which is in the mainet/testnet. We should prepare a deploy file which allow us to deploy the contract in the testent, mainet and the delompent network.

* We should avoid hardcoded addresses in the contract. We should give the adresses through the constructor


## Add a network to brownie
* ```brownie networks list```:  List all the networks saved
* ```brownie networks add [environment] [name] host=[host] chainid=[chaiId]```: To add a new network

### Test in networks
```brownie test --network <network-name>```

### Test in mainets forks
If we fork a blockchain, we can use all the contracts inside the network BEFORE the fork. for this we will need to add a new network which will be out fork. We can get our for from alchemy and the add it using the next line ```brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/API-KEY accounts=10 mnemonic=brownie port=8546```

This will also create fake account which we can access using accounts from brownie

# Lesson 7: Lottery
## address payable
* Only **address payable** can use the methods: *send()*, *transfer()* and *call()*
* An address can be casted to a **address payable**:
```solidity
address addr1 = msg.sender;
address payable addr2 = addr1; // Incorrect
address payable addr3 = address(uint160(addr1)); // Correct since Solidity >= 0.5.0
address payable addr4 = payable(addr1); // Correct since Solidity >= 0.6.0
```
* More information [here](https://ethereum.stackexchange.com/questions/64108/whats-the-difference-between-address-and-address-payable)

## Insecure randomness
[News](https://es.cointelegraph.com/news/85-million-meebits-nft-project-exploited-attacker-nabs-700-000-collectible)
[Explanation](https://forum.openzeppelin.com/t/understanding-the-meebits-exploit/8281/2) (see PatrickAlphaC answer)
```solidity
uint(
    keccak256( //Hashing function
        abi.encodePacked(
            nonce, // Is predictable (AKA, transaction number)
            msg.sender, //Not random
            block.difficulty, //Can be manipulated by miners
            block.timestamp // Is predictable
        )
    )
)
```

## Secure randomness
* Need to use an oracle. For instance: Chainlink VRF

### Using Chailink VRF
* To use the Chainlink VRF we need to provide the contract with the appropiate token (LINK).
* The contract which will use the random number has to be **VRFConsumerBase**
```solidity
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase{
    //...
}
```
* To get the random number we need to give the constructor 2 parameters and use the **VRFConsumerBase** constructor
```solidity
constructor(
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyHash
    ) public VRFConsumerBase(_vrfCoordinator,_link){
        //...
    }
```
* The **VRFConsumerBase** will allow us to use 2 methods:
    * requestRandomness(keyHash,fee): This method will request the VRF node a random number, and give us a requestId (byte32 type) 
    * fulfillRandomness(bytes32 _requestId, uint256 _randomness): A method to override, will be called by the VRFCoordinator. The _randomness will be a random number

* It is important that the contract which call the *requestRandomness* function has been funded with link. We can do that with this python function:
```python
from brownie import (
    interface) #It is importan to add the LinkTokenInterface to the interface folder

def fund_with_link(contract_address, sender_account, link_contract, amount=(1* 10**18)):
    #opcion 1
    # tx = link_contract.transfer(contract_address,amount, {"from":sender_account})
    
    #Opcion 2
    link_token_contract = interface.LinkTokenInterface(link_contract.address)

    print("Funding "+contract_address+" with LINK")
    tx = link_token_contract.transfer(contract_address,amount, {"from":sender_account})
    
    link_amount=amount/ (10**18)
    tx.wait(1)

    print(contract_address+": Funded with "+str(link_amount)+" link")
    return tx
```

## Events
Events aren't accesible for smart contracts, but they are stored in the blockchain

## Testing
### Unit tests
A way of testing the smallest pieces of code in an isolated instance.
We want to test every line of our smart contract

### Integration testing
A way of testing across multiple complex systems

# Lesson 8
## Baking a contract in brownie
Brownie allow us create standarize projects. Currently there are 12, for more information about them [here](https://github.com/brownie-mix)
To create one of this project only use the line ```brownie bake STANDARIZE-PROJECT-NAME```