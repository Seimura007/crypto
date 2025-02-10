pragma solidity ^0.8.0;

contract MustFasterCoin {
    string public constant name = "Must Faster Coin";
    string public constant symbol = "MFC";
    uint public totalSupply;
    
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    mapping(address => bool) public managers;

    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed spender, uint value);
    event Mint(address indexed to, uint value);
    event Burn(address indexed from, uint value);

    constructor(uint initialSupply) {
        totalSupply = initialSupply;
        balances[msg.sender] = totalSupply;
        managers[msg.sender] = true; // назначение прав на управление токенами
    }

    modifier onlyManager() {
        require(managers[msg.sender], "Не достаточно прав");
        _;
    }

    function transfer(address to, uint value) public {
        require(to != address(0), "Неправильный адрес");
        require(value > 0 && balances[msg.sender] >= value, "Недостаточно токенов для перевода");
        balances[msg.sender] -= value;
        balances[to] += value;
        emit Transfer(msg.sender, to, value);
    }

    function approve(address spender, uint value) public returns (bool) {
        require(spender != address(0) && balances[msg.sender] >= value, "Неправильный адрес");
        allowed[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transferFrom(address from, address to, uint value) public returns (bool) {
        require(from != address(0) && to != address(0) && value > 0, "Неправильные параметры");
        require(balances[from] >= value && allowed[from][msg.sender] >= value, "Недостаточно токенов");
        
        balances[from] -= value;
        balances[to] += value;
        allowed[from][msg.sender] -= value;
        emit Transfer(from, to, value);
        return true;
    }

    function balanceOf(address owner) public view returns (uint) {
        return balances[owner];
    }

    function allowance(address owner, address spender) public view returns (uint) {
        return allowed[owner][spender];
    }

    function mint(address to, uint value) public onlyManager {
        require(to != address(0), "Неправильный адрес");
        balances[to] += value;
        totalSupply += value;
        emit Mint(to, value);
    }

    function burn(uint value) public {
        require(balances[msg.sender] >= value, "Недостаточно токенов для сжигания");
        balances[msg.sender] -= value;
        totalSupply -= value;
        emit Burn(msg.sender, value);
    }

    function addManager(address newManager) public onlyManager {
        managers[newManager] = true;
    }

    function removeManager(address manager) public onlyManager {
        managers[manager] = false;
    }
}
