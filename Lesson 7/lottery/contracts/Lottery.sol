// SPDX-License-Identifier: MIT 

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";


contract Lottery is Ownable, VRFConsumerBase{
    // To use SafeMathChainlink for all our uint256 operations
    using SafeMathChainlink for uint256; 

    address payable[] public players;
    uint256 public randomness;
    uint256 public entryFeeInUSDWEI;
    address payable public recentWinner;
    AggregatorV3Interface public ethUsdPriceFeed;
    mapping(address => uint256) public addressToNumber;
    uint256 blockStart;
    uint256 blockEnd;
    enum LOTTERY_STATE {
        OPEN,
        CLOSE,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyHash;

    //----EVENTS
    event RequestedRandomness(bytes32 requestId);

    modifier onlyOpenLottery{
        require(lottery_state==LOTTERY_STATE.OPEN);
        _;
    }
    
    constructor(
        uint256 _entryFeeInUSD,
        address _priceFeedContract,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyHash
    ) public VRFConsumerBase(_vrfCoordinator,_link){
        //admin=msg.sender;
        //owner=msg.sender;
        fee=_fee;
        keyHash=_keyHash;
        entryFeeInUSDWEI=_entryFeeInUSD * 10**18;
        ethUsdPriceFeed= AggregatorV3Interface(_priceFeedContract);
        lottery_state=LOTTERY_STATE.CLOSE;
    }


    function enter() public payable onlyOpenLottery{
        //Require a minimum value
        require(msg.value >= getEntranceFee());
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns(uint256){
        (,int256 ethPriceInUSDWEI,,,) = ethUsdPriceFeed.latestRoundData();
        uint256 ethPriceInUSDWEICorrected = uint256(ethPriceInUSDWEI* (10**10));

        //We need to avoid decimals when we operate, so previosly we need to
        //Multiply the numerator by 10**18
        uint256 entraceFeeInETHWEI= (entryFeeInUSDWEI * 10**18 ).div(ethPriceInUSDWEICorrected);
        return entraceFeeInETHWEI;
    }

    function startLottery() public onlyOwner{
        require(lottery_state== LOTTERY_STATE.CLOSE, "Can't start a new lottery yet");
        lottery_state=LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner onlyOpenLottery{
        //uint(
        //    keccak256( //Hashing function
        //        abi.encodePacked(
        //            nonce, // Is pre dictable (AKA, transaction number)
        //            msg.sender, //Not random
        //            block.difficulty, //Can be manipulated by miners
        //            block.timestamp // Is predictable
        //        )
        //    )
        //) % players.length;
        lottery_state=LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId=requestRandomness(keyHash,fee);
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override{
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER, "You aren't yet there");
        require(_randomness>0, "random not found");
        //To select a winner we need to chose one in our players array
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner=players[indexOfWinner];
        recentWinner.transfer(address(this).balance);
        players= new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSE;
        randomness=_randomness;
    }
    

    //function getStartLottery() public view returns(uint256)

    //function getEndLottery() public view returns(uint256){

    //function decideWinner() private returns(uint256)
}