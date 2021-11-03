// SPDX-License-Identifier: MIT 

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe{
    // To use SafeMathChainlink for all our uint256 operations
    using SafeMathChainlink for uint256; 
    
    mapping(address => uint256) public addressToAmountFunding;
    address[] funders;
    address public owner;
    AggregatorV3Interface public priceFeed;
    
    modifier onlyOwner {
        require(msg.sender==owner);
        _;
    }
    
    constructor(address _priceFeedContract) public {
        owner=msg.sender;
        // 0x9326BFA02ADD2366b30bacB125260Af641031331 Kovan
        priceFeed= AggregatorV3Interface(_priceFeedContract);
    }
    
    function fund() public payable{
        uint256 minimumUSDWei = 5 * (10**18);
        
        //If the condition is true, the execution goes on. If not, it stops and give the specified error message
        require(getConversionRate(msg.value)>=minimumUSDWei, "You need to spent more ETH!");
        addressToAmountFunding[msg.sender] += msg.value;
        funders.push(msg.sender);
        
        // What the ETH -> USD conversion rate?
    }
    
    function getVersion() public view returns (uint256){
        return priceFeed.version();
    }
    
    
    function getPrice() public view returns (uint256){
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer * (10**10)); //value in wei unit for USD (1 ETH = answer * 10**10 USD wei)
        //4.195,48 10 79 66
    }
    
    /*
        @ return ethWeiAmount in usdWei amount
    */
    function getConversionRate(uint256 ethWeiAmount) public view returns (uint256){
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsdWei = (ethPrice * ethWeiAmount)/ (10**18);
        return ethAmountInUsdWei;
    }
    
    
    
    function withdraw() public payable onlyOwner{
        msg.sender.transfer(address(this).balance);
        for (uint256 funderIndex = 0; funderIndex< funders.length; funderIndex++) {
            address funder = funders[funderIndex];
            addressToAmountFunding[funder]=0;   
        }
        funders = new address[](0);
    }
    
    function getEntranceFee() public view returns (uint256) {
        // mimimumUSD
        uint256 mimimumUSD = 5 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (mimimumUSD * precision) / price;
    }
}