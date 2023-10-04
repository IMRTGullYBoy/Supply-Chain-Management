## Group information: 
Nagalla Sai Charan - 2020A7PS0182H <br/>
Venkat Rohith Pamarti -  2020A7PS0100H <br/>
S V S Rahul      -       2020A7PS0204H <br/>
Bangi Karthik -          2020A7PS0164H <br/>
Amogh Moses - 2020A7PS0000H <br/>

### Libraries Used: 
random - for using random library to assign random time values for each node with in a given specified time<br/><br/>
ecdsa (Elliptic Curve Digital SIgnature Algorithm) - to create public and private keys for validating the new nodes<br/><br/>
time - for generating timestamps and random time and sleep function<br/><br/>
hashlib - for using SHA256 to hash the block<br/><br/>
json - to convert the format of the message<br/><br/>

### Installations:

Install pip using `npm install pip`
Install ecdsa using `pip install ecdsa`

## Problem statement: 
In a manufacturing company that produces over ten different products, there are ongoing distribution challenges when delivering products to clients.
Manufacturer distributes the products to the distributors ordered by clients, but he is not aware if the product has been delivered succesfully or not, as client or distrubutors can lie about the delivery status. 
Your task is to create a supply chain management system that ensures products successfully reach clients through the involvement of distributors.
To create a decentralized system (Block Chain) where distributors and clients act as Nodes and the transactions happening between distributors and clients to be secured. 

## Features: 
1. New users can be registered either as a client or a distributor. <br/>
2. The client should be able to order products  <br/>
3. The Distributor can dispatch the products ordered by clients <br/>
4. To improve the security of blockchain, consensus algorithm (PoS) has been implemented.<br/>
5. Merkle root is implemented to calculate hash of all the transactions in a block<br/>
6. QR Code can be generated to check the status of a product delivery <br/>

### Structure of Transaction: 
ManufacturerId, ClientId, DistributorId, Price, Time stamp of the transaction. <br/>

### Structure of a block in blockchain: 
Block Index ,Timestamp, Merkle root, Hash of the previous block, Transactions(2), Proof. <br/>

## Directions to use: 
To execute, run python3 blockchain.py <br/> 
You have 5 options (1 to 5): Enter <br/>
'1' to register a new node(User) <br/>
'2' to Login into the system<br/>
'3' to View Block Chain <br/>
'4' to verify the blockchain (valid or not) <br/>
'5' to exit from the blockchain <br/> <br/>

## PoS Algorithm<br/>
Proof of Stake (PoS) is a blockchain consensus algorithm where validators are chosen to create new blocks and validate transactions based on the amount of cryptocurrency they hold and are willing to "stake" as collateral. 
<br/>
Validators with more staked tokens have a higher chance of being selected.
<br/>
PoS is energy-efficient compared to Proof of Work (PoW) and incentivizes network security through staking, as validators risk losing their collateral if they act dishonestly.
<br/>
It is a fundamental mechanism in many blockchain networks for securing and governing decentralized systems.
<br/>

## Description of functions: 
  1. Reg_User() - This is a function used to take inputs from the user and validate. <br/>
        1. add_User(userId, userName, balance, security, role) - Adds the user and his properties to the users list.<br/>
        1. validate_User(publickey, signature, userId, userName) - verifies the values of hash.<br/>
  2. Login() - This function checks whether the userId and password are matching and redirects to dashboard of their respective roles. <br/>
  3. add_Transact(manufactureId, clientId, distributorID, price) - validates the transactions and adds it to list of transactions if it is correct. <br/> 
  4. md(), cd(), dd() - These functions shows the Manufacturer's, Client's, Distributor's dashboards based on their role. <br/>
  5. display_blockchain() - This function is used to display all the blocks of the transaction. <br/> 
  6. chain_valid() - This function is used to check whether the blockchain is valid or not. <br/>
  7. create_block() - calculates the one who has the highest stake among all of the nodes and new_block is invoked. <br/>
        1. new_block(proof, prevhash = none) - calculate merkle roots and creates the block with index , timestamp, transactions, merkle root, proof, prevhash and cryptographically links it to previous block.
        <br/>
        1. calcate_hash(arg) - encrypts the given argument with SHA-256 and returns the hash value. <br/>
      
  8. generate_qr_code() - This functions generates the QR code to show the status of the Product.  
 