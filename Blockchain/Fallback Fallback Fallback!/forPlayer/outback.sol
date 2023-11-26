// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

contract Setup {
    bool private solved;
    constructor() payable {
        solved = false;
    }

    fallback() external payable{
        solved = true;
    }

    function isSolved() external view returns (bool) {
        return solved;
    }
}