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

# contract address for weth
weth_address = '0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6'



# do aave stuff
def aave_deposit(amount):
    # get a lending pool
    lending_pool = aave_get_lending_pool()

    # first we have to get the lending pool address
    aave_approve_erc20(lending_pool.address, amount)
    print(lending_pool.address)

    # get the nonce for this transaction
    nonce = web3.eth.getTransactionCount(my_address)

    #temp#

    function_call = lending_pool.functions.supply(weth_address, web3.toWei(amount, "ether"), my_address, 0)

    # deposit our tokens
    transaction = function_call.build_transaction(#lending_pool.functions.supply(weth_address, web3.toWei(amount, "ether"), my_address, 0).buildTransaction(
        {
            "chainId": 5,
            "from": my_address,
            "nonce": nonce,
        }
    )

    # sign the transaction
    signed_tx = web3.eth.account.sign_transaction(transaction, priv_address)

    # send the transaction and get the hash
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print("Deposited " + str(amount) + " into aave")
    print_aave_user_data(lending_pool)


# print all user data to test if we really did deposit
def print_aave_user_data(lending_pool):
    userdata = lending_pool.functions.getUserAccountData(my_address).call()
    print(userdata)


# get the address of the lending pool we should use
def aave_get_lending_pool():
    # contract address of the lending pool address provider
    pool_addresses_provider_address = '0xc4dCB5126a3AfEd129BC3668Ea19285A9f56D15D'
    #pool_addresses_provider_address = '0x5E52dEc931FFb32f609681B8438A51c675cc232d'

    # pool address provider contract
    pool_addresses_provider = web3.eth.contract(address = pool_addresses_provider_address, abi = lending_pool_addresses_provider_abi)

    # our specific pool address
    lending_pool_address = pool_addresses_provider.functions.getPool().call()

    # contract for the given pool
    lending_pool = web3.eth.contract(address = lending_pool_address, abi = lending_pool_abi)
    return lending_pool

# get approval for aave to take "amount" of weth from your wallet
def aave_approve_erc20(lending_pool_address, amount):
    # get the weth contract so we can interact with our tokens
    weth = web3.eth.contract(address = weth_address, abi = weth_abi)
    
    # get the nonce for this transaction
    nonce = web3.eth.getTransactionCount(my_address)

    # let the lending_pool we're using actually move our tokens around
    transaction = weth.functions.approve(lending_pool_address, web3.toWei(amount, "ether")).buildTransaction(
        {
            "chainId": 5,
            "from": my_address,
            "nonce": nonce
        }
    )

    # sign transaction with private key
    signed_tx = web3.eth.account.sign_transaction(transaction, private_key = priv_address)

    # send the transaction and record the hash
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # wait for receipt I guess?
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print(str(amount) + " tokens approved for aave")

    #debug#
    allowance = weth.functions.allowance(my_address, lending_pool_address).call()
    print("Allowance: " + str(allowance))
    #debug#
    return


#mints wrapped eth (weth) from eth
def get_weth(value = .001):
    # get the weth contract address
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

aave_deposit(.05) #debug#