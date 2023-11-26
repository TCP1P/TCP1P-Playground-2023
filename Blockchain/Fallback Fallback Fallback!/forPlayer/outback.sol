// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract outback {
    string private flag;
    bool public solved;

    constructor(){
        flag = "Trial Flag";
    }

    function isSolved() external view returns(string memory) {
        require(solved, "You have not solved the challenge!");
        return flag;
    }

    fallback() external payable {
        solved = true;
    }

}
