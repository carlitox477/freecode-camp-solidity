// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

// NFT, we can get any of the 3 IMGS randomly

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvanceCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyHash;
    uint256 public fee;
    enum Breed{PUG, SHIBA_IMU,ST_BERNARD}
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;

    //Events
    event RequestCollectible(bytes32 indexed requestId, address requester);
    event BreedAssigned(uint256 indexed tokenId, Breed breed);


    constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee) public
    VRFConsumerBase(_vrfCoordinator, _linkToken)
    ERC721("Doggie","Dog"){
        keyHash=_keyhash;
        fee=_fee;
        tokenCounter=0;
    }

    function createCollectible() public returns(bytes32){
        require(LINK.balanceOf(address(this)) >= fee, "Not enough LINK - fill contract with faucet");        
        
        bytes32 requestId=requestRandomness(keyHash, fee);
        requestIdToSender[requestId]=msg.sender;
        emit RequestCollectible(requestId,msg.sender);
        return requestId;
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness) internal override {
        Breed breed = Breed(randomness % 3);
        uint256 newTokenId=tokenCounter;
        address nftOwner=requestIdToSender[requestId];

        tokenIdToBreed[newTokenId]=breed;
        _safeMint(nftOwner,newTokenId);
        tokenCounter=tokenCounter+1;

        BreedAssigned(newTokenId,breed);
        
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public{
        require(_isApprovedOrOwner(_msgSender(),tokenId), "ERC721: transfer caller is not owner nor approved");
        _setTokenURI(tokenId,_tokenURI);
    }
}