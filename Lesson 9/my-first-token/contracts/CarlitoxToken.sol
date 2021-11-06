// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
//Where name and symbol goes in ERC20?

contract CarlitoxToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("Carlitox Token", "CTX") {
        _mint(msg.sender, initialSupply);
    }
}