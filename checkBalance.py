from web3 import Web3

# goerli infura node
provider = 'https://goerli.infura.io/v3/19422f0b6f114fcea2b8b0b8d480728e'
web3 = Web3(Web3.HTTPProvider(provider))

weth_address = '0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6'

account_1 = '0xE4c3ff85A999178B923919954b7fFA7492FA50C7'

# erc20 abi
min_abi = [
  {
    "constant": True,
    "inputs": [{ "name": "_owner", "type": "address" }],
    "name": "balanceOf",
    "outputs": [{ "name": "balance", "type": "uint256" }],
    "type": "function",
  }
]

weth = web3.eth.contract(address = weth_address, abi = min_abi)


# ether balance here is formatted in ether, 
eth_balance = web3.fromWei(web3.eth.getBalance(account_1), "ether")
print("eth: " + str(eth_balance))

# weth balance
weth_balance = web3.fromWei(weth.functions.balanceOf(account_1).call(), "ether")
print("weth: " + str(weth_balance))
