 pragma solidity ^0.4.17;

contract Lottery {
    uint public ticket_cost;
    uint public latestBlockNum;
    uint public lotteryPrice;

    uint32 public globalXOR;
    
    address public owner;
    bytes32 public hash;

    address [] approvedTickets;
    address [] winners;
    
    mapping(bytes32 => address) ticketHash;
    mapping(address => uint) playerBoughtTicketNum;

    uint32 public submissionTime;   
    uint32 public submitSecretTime; 
    uint32 public payoutTime;

    uint   public selectedIndex;
    

    function Lottery() { //Adternative signature: function Lottery(uint ticketPrice, submissionTime, submitSecretTime, payoutTime) {
	ticket_cost         = 100000000000000000; // 0.1 ether == 100000000000000000 wei  
	lotteryPrice        = 0;
	owner               = msg.sender;
	latestBlockNum      = block.number;

	submissionTime   = 5; //5760; //Worst case around ~1 Day.
	submitSecretTime = 5; //2400; //Worst case around ~1 hour.
	payoutTime       = 2400; //Worst case around ~1 hour.
    }

    function buyLotteryTicket(bytes32 secretHash, uint ticketNum) payable returns (bool success)
    {
	if( (block.number - latestBlockNum > submissionTime) || //Checks is it the lottery ticket buy time completed or not.
	    msg.value != ticket_cost * ticketNum             ||  //Double check for the paid money.
	    ticketHash[secretHash] != 0                      ||
	    ticketNum > 10                                   ||
	    ticketNum == 0 )
	    revert();
	    		

	ticketHash[secretHash]             = msg.sender;
	playerBoughtTicketNum[msg.sender] += ticketNum;
	lotteryPrice                      += msg.value;
	LogNewLotteryPrice(lotteryPrice);	
	LogBuyLottery(block.number, msg.sender);
	return true;
    }


    function submitSecretHashNumber(uint32 secretNum) returns (bool success)
    {

	if( playerBoughtTicketNum[msg.sender] == 0         ||  
	    block.number-latestBlockNum < submissionTime   ||
	    block.number-latestBlockNum >= submissionTime+submitSecretTime) {
	    revert(); 
	}

	bytes32 secretSHA;
	if( ticketHash[ secretSHA=keccak256(secretNum, msg.sender) ] == msg.sender ) { //Approved.
	    globalXOR = globalXOR ^ secretNum;	  
	    delete ticketHash[secretSHA]; //First clean. Freed memory is rewarded and should be set to null.
		
	}
	else
	    revert();
	    
	for(uint32 i=0; i< playerBoughtTicketNum[msg.sender]; i++)
	    approvedTickets.push(msg.sender);

	delete playerBoughtTicketNum[msg.sender]; //Memory cleaned and equaled to 0.
	return true;
    }


    function payOut() returns (bool success) //Caller gets his gas price.
    {
	if( block.number-latestBlockNum < submissionTime+submitSecretTime || msg.sender != owner )
	  revert();

	selectedIndex = globalXOR % approvedTickets.length;
	
	address winnerBuyer = approvedTickets[ selectedIndex ];
	winners.push(winnerBuyer);

	if(!winnerBuyer.send(lotteryPrice))
	  revert();
	
	latestBlockNum      = block.number;

	LogWinner(block.number, winnerBuyer, lotteryPrice);
	LogApprovedTickets(approvedTickets);

	lotteryPrice = 0;
	delete approvedTickets;
	delete globalXOR;		    
	return true;
    }

    function dummyTx(){} //Populus to increment block.number.

    // --------------------------------------------------GETTERS----------------------------------

    function getSelectedIndex() constant returns (uint)
    {
	return selectedIndex;
    }

    function getGlobalXOR() constant returns (uint)
    {
	return globalXOR;
    }

    function getLotteryPrice() constant returns (uint)
    {
	return lotteryPrice;
    }
    
    function getOnGoingBlockNumber() constant returns (uint)
    {
	return latestBlockNum;
    }

    function getLotteryTicketPrice() constant returns (uint)
    {
	return ticket_cost;
    }

    // Returns all the winners
    function getWinner() constant returns (address[])
    {
	return winners;
    }
    // Returns all the approved Tickets
    function getApprovedTickets() constant returns (address[])
    {
	return approvedTickets;
    }

    function getTest() constant returns (address, bytes32)
    {
	return (owner, hash);
    }

    event LogBuyLottery      (uint blocknumber, address buyer);
    event LogWinner          (uint blocknumber, address winner, uint lotteryPrice);
    event LogApprovedTickets (address[] approvedTickets);
    event LogNewLotteryPrice (uint newLotteryPrice);

}
