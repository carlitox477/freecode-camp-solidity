// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";

contract Box{
    uint256 private value;

    event ValueChanged(uint256 newValue);

    function store(uint256 newValue) public{
        value= newValue;
        emit ValueChanged(newValue);
    }

    function retrieve() public view returns(uint256){
        return value;
    }
}