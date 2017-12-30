def sha3Converter(randomNumber, addressUser,web3):    
    print str(randomNumber)+" "+addressUser
    randomNumber = hex(randomNumber)[2:]
    hashStr =  randomNumber.zfill(8) + addressUser[2:]
    return web3.sha3(hashStr)    
    
    
def test_greeter(web3, accounts, chain):
    myContract, _ = chain.provider.get_or_deploy_contract('Lottery')
    tickerPrice  = myContract.call().getLotteryTicketPrice();

    print accounts
    ## 1. BUY LOTTERY ROUND
    ##----------
    web3.eth.defaultAccount = accounts[0]; 
    secretHash = sha3Converter(14, web3.eth.defaultAccount, web3)
    hexData    = secretHash[2:].decode("hex");
    #print secretHash          
    
    set_txn_hash = myContract.transact({"from": web3.eth.defaultAccount, "value": web3.toWei(3*tickerPrice, "wei") }).buyLotteryTicket(hexData, 3)
    chain.wait.for_receipt(set_txn_hash);                                                    
    print "BlockNumber: " + str(web3.eth.blockNumber);
   
    web3.eth.defaultAccount = accounts[1];
    secretHash = sha3Converter(25, web3.eth.defaultAccount, web3)
    hexData    = secretHash[2:].decode("hex");
    

    set_txn_hash = myContract.transact({"from": web3.eth.defaultAccount, "value": web3.toWei(3*tickerPrice, "wei") }).buyLotteryTicket(hexData, 3)
    chain.wait.for_receipt(set_txn_hash);                                                    
    print "BlockNumber: " + str(web3.eth.blockNumber);
    ##----------
    
    for i in range(0, 5):
        myContract.transact().dummyTx();

    ## 2. REVEAL ROUND:    
    ##----------
    print "BlockNumber: " + str(web3.eth.blockNumber);
    web3.eth.defaultAccount = accounts[0];
    set_txn_hash = myContract.transact().submitSecretHashNumber(14);

    print "BlockNumber: " + str(web3.eth.blockNumber);
    web3.eth.defaultAccount = accounts[1];
    set_txn_hash = myContract.transact().submitSecretHashNumber(25);
    ##----------

    ## 3. PAYOUT ROUND:    
    ##----------
    lotteryPrice = myContract.call().getLotteryPrice()
    print "lotteryPrice: " + str(lotteryPrice)

    web3.eth.defaultAccount = accounts[0];
    set_txn_hash = myContract.transact().payOut();
    #set_txn_hash = myContract.transact().payOut(); #Gives error.
    ##----------

    XOR = myContract.call().getGlobalXOR()
    print "XOR: " + str(XOR)

    #vaL = 14 ^ 25
    #print vaL

    winners = myContract.call().getWinner()
    print "Winners: " 
    print winners

    approvedTickers = myContract.call().getApprovedTickets()
    print approvedTickers
    

    ##############################################################################################
    # Next CYLE:
    ## 1. BUY LOTTERY ROUND
    ##----------
    web3.eth.defaultAccount = accounts[1]; 
    secretHash = sha3Converter(14, web3.eth.defaultAccount, web3)
    hexData    = secretHash[2:].decode("hex");
    #print secretHash          
    
    set_txn_hash = myContract.transact({"from": web3.eth.defaultAccount, "value": web3.toWei(3*tickerPrice, "wei") }).buyLotteryTicket(hexData, 3)
    chain.wait.for_receipt(set_txn_hash);                                                    
    print "BlockNumber: " + str(web3.eth.blockNumber);
   
    web3.eth.defaultAccount = accounts[0];
    secretHash = sha3Converter(25, web3.eth.defaultAccount, web3)
    hexData    = secretHash[2:].decode("hex");
    

    set_txn_hash = myContract.transact({"from": web3.eth.defaultAccount, "value": web3.toWei(3*tickerPrice, "wei") }).buyLotteryTicket(hexData, 3)
    chain.wait.for_receipt(set_txn_hash);                                                    
    print "BlockNumber: " + str(web3.eth.blockNumber);
    ##----------
    
    for i in range(0, 5):
        myContract.transact().dummyTx();

    ## 2. REVEAL ROUND:    
    ##----------
    print "BlockNumber: " + str(web3.eth.blockNumber);
    web3.eth.defaultAccount = accounts[1];
    set_txn_hash = myContract.transact().submitSecretHashNumber(14);

    print "BlockNumber: " + str(web3.eth.blockNumber);
    web3.eth.defaultAccount = accounts[0];
    set_txn_hash = myContract.transact().submitSecretHashNumber(25);
    ##----------

    ## 3. PAYOUT ROUND:    
    ##----------  
    web3.eth.defaultAccount = accounts[0];

    approvedTickers = myContract.call().getApprovedTickets()
    print approvedTickers

    XOR = myContract.call().getGlobalXOR()
    print "XOR: " + str(XOR)

    lotteryPrice = myContract.call().getLotteryPrice()
    print "lotteryPrice: " + str(lotteryPrice)
    

    set_txn_hash = myContract.transact().payOut();
    #set_txn_hash = myContract.transact().payOut(); #Gives error.
    ##----------

    (a, b) = myContract.call().getTest()
    b = b.encode('latin-1')
    b = b.encode("hex")
    print("--------")
    print(a)
    print(b)    

    winners = myContract.call().getWinner()
    print "Winners: " 
    print winners

    approvedTickers = myContract.call().getApprovedTickets()
    print approvedTickers

    
    #vaL = 14 ^ 25
    #print vaL   
    #100000000000000000 WEI = 100 FINNEY
