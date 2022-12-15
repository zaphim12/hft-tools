from web3 import Web3
from abis import weth_abi
from abis import (
    lending_pool_addresses_provider_abi,
    lending_pool_abi,
    erc20_abi
)

# get a Web3 object using infura node
provider = 'https://goerli.infura.io/v3/19422f0b6f114fcea2b8b0b8d480728e'
web3 = Web3(Web3.HTTPProvider(provider))

# literally just my public key and private key
my_address = '0xE4c3ff85A999178B923919954b7fFA7492FA50C7'
priv_address = '20581c4277871777beeabe069b2304fe0223d6018200dd50188cbb1a3e3e7f54'


# do aave stuff
def aave_deposit():
    


#mints wrapped eth (weth) from eth
def get_weth(value = .001):
    # contract address for weth
    weth_address = '0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6'
    
    nonce = web3.eth.getTransactionCount(my_address)
    weth = web3.eth.contract(address = weth_address, abi = weth_abi)

    # form the transaction
    transaction = weth.functions.deposit().buildTransaction(
        {
            "chainId": 5,
            "from": my_address,
            "nonce": nonce, 
            "value": web3.toWei(value, "ether")
        }
    )

    # sign the transaction
    signed_tx = web3.eth.account.sign_transaction(
        transaction, private_key = priv_address
    )

    # send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print("Tx hash: " + str(web3.toHex(tx_hash)))
