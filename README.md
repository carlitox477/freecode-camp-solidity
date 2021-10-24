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
pragma solidity 0.6.0; //We use solidity 0.6.0
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




# Financial decisions
* Invest in cryptos. If it hasn't explode yet it main launchpad and dex are good options too.
* Decentralization gives value to a blockchain

