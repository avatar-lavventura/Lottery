def sha3Converter(randomNumber, addressUser,web3):    
    print str(randomNumber)+" "+addressUser
    randomNumber = hex(randomNumber)[2:]
    hashStr =  randomNumber.zfill(8) + addressUser[2:]
    return web3.sha3(hashStr)    
    
    
def test_greeter(web3, accounts, chain):
    myContract, _ = chain.provider.get_or_deploy_contract('Lottery')
    tickerPrice  = myContract.call().getLotteryTicketPrice();
    print "tickerPrice: " + str(tickerPrice);

    print "UserA: " + accounts[1];
    print "UserB: " + accounts[2];
    
    #print( web3.eth.getBalance(accounts[1]) );
    #print( web3.eth.getBalance(accounts[2]) );

    ## 1. BUY LOTTERY ROUND
    ##----------
    web3.eth.defaultAccount = accounts[1];
    
    secretHash = sha3Converter(12345, web3.eth.defaultAccount, web3)
    hexData    = secretHash[2:].decode("hex");
    #print secretHash          
    
    set_txn_hash = myContract.transact({"from": web3.eth.defaultAccount, "value": web3.toWei(3*tickerPrice, "wei") }).buyLotteryTicket(hexData, 3)
    chain.wait.for_receipt(set_txn_hash);                                                    
    #print "BlockNumber: " + str(web3.eth.blockNumber);
   
    web3.eth.defaultAccount = accounts[2];
    secretHash = sha3Converter(54321, web3.eth.defaultAccount, web3)
    hexData    = secretHash[2:].decode("hex");
    

    set_txn_hash = myContract.transact({"from": web3.eth.defaultAccount, "value": web3.toWei(3*tickerPrice, "wei") }).buyLotteryTicket(hexData, 3)
    chain.wait.for_receipt(set_txn_hash);                                                    
    #print "BlockNumber: " + str(web3.eth.blockNumber);
    ##----------
    
    for i in range(0, 5):
        myContract.transact().dummyTx();

    ## 2. REVEAL ROUND:    
    ##----------
    #print "BlockNumber: " + str(web3.eth.blockNumber);
    web3.eth.defaultAccount = accounts[1];
    set_txn_hash = myContract.transact().submitSecretHashNumber(12345);

    #print "BlockNumber: " + str(web3.eth.blockNumber);
    web3.eth.defaultAccount = accounts[2];
    set_txn_hash = myContract.transact().submitSecretHashNumber(54321);
    ##----------

    ## 3. PAYOUT ROUND:    
    ##----------
    #print( web3.eth.getBalance(accounts[1]) );
    #print( web3.eth.getBalance(accounts[2]) );
    
    lotteryPrice = myContract.call().getLotteryPrice()
    print "lotteryPrice: " + str(lotteryPrice)

    XOR = myContract.call().getGlobalXOR()
    print "XOR: " + str(XOR)

    winners = myContract.call().getWinner()

    web3.eth.defaultAccount = accounts[0];
    set_txn_hash = myContract.transact().payOut();
    #set_txn_hash = myContract.transact().payOut(); #Gives error.
    ##----------

    index = myContract.call().getSelectedIndex();
    print "Index: " + str(index);
    print "Winners: " 
    print winners

    #approvedTickers = myContract.call().getApprovedTickets()
    #print approvedTickers

    print "--------------------------"
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
    #print "BlockNumber: " + str(web3.eth.blockNumber);
   
    web3.eth.defaultAccount = accounts[2];
    secretHash = sha3Converter(25, web3.eth.defaultAccount, web3)
    hexData    = secretHash[2:].decode("hex");
    

    set_txn_hash = myContract.transact({"from": web3.eth.defaultAccount, "value": web3.toWei(3*tickerPrice, "wei") }).buyLotteryTicket(hexData, 3)
    chain.wait.for_receipt(set_txn_hash);                                                    
    #print "BlockNumber: " + str(web3.eth.blockNumber);
    ##----------
    
    for i in range(0, 5):
        myContract.transact().dummyTx();

    ## 2. REVEAL ROUND:    
    ##----------
    #print "BlockNumber: " + str(web3.eth.blockNumber);
    web3.eth.defaultAccount = accounts[1];
    set_txn_hash = myContract.transact().submitSecretHashNumber(14);

    #print "BlockNumber: " + str(web3.eth.blockNumber);
    web3.eth.defaultAccount = accounts[2];
    set_txn_hash = myContract.transact().submitSecretHashNumber(25);
    ##----------

    ## 3. PAYOUT ROUND:    
    ##----------  
    web3.eth.defaultAccount = accounts[0];

    approvedTickers = myContract.call().getApprovedTickets()
    #print approvedTickers

    XOR = myContract.call().getGlobalXOR()
    print "XOR: " + str(XOR)

    lotteryPrice = myContract.call().getLotteryPrice()
    print "lotteryPrice: " + str(lotteryPrice)
    

    set_txn_hash = myContract.transact().payOut();
    #set_txn_hash = myContract.transact().payOut(); #Gives error.
    ##----------

    index = myContract.call().getSelectedIndex();
    print "Index: " + str(index);
    winners = myContract.call().getWinner()
    print "Winners: " 
    print winners

    #approvedTickers = myContract.call().getApprovedTickets()
    #print approvedTickers  

    ##---
    '''
    (a, b) = myContract.call().getTest()
    b = b.encode('latin-1')
    b = b.encode("hex")
    print("--------")
    print(a)
    print(b)    
    '''
