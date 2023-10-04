import hashlib
import json
from time import time
from time import sleep
import sqlite3 as sl
from ecdsa import SigningKey
import random
import qrcode
from PIL import Image

class BlockChain(object):
    bf = 2
    dict_obj={}
    elapsedTime_dictobj={}
    property_owner={}
    global leadernode
    def __init__(self):
        
        self.chain = []
        self.complete_transactions = []
        self.Users = []
        self.Products = []
        self.new_block(100, "Gensis block")
        self.add_User('1','Admin','Root',0,0,3)

    def calculate_hash(self, hh):
        string_object = json.dumps(hh, sort_keys=True)
        trans_string = string_object.encode()

        raw_hash = hashlib.sha256(trans_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'merkel_root': '',
            'proof': proof,
            'transactions': self.complete_transactions,
            #Input of previous_hash necessary for genesis block / cryptographically linking the previous block
            'previous_hash': previous_hash or self.calculate_hash(self.chain[-1]),
        }
        if(len(self.complete_transactions) != 0):
            #Calculation of merkel root for the two transactions in the block
            block['merkel_root'] = self.calculate_hash(self.calculate_hash(self.complete_transactions[0]) + self.calculate_hash(self.complete_transactions[1]))
        #Confirming the complete_transactions
        self.complete_transactions = []
        #Appending block to the list
        self.chain.append(block)
        return block
    
    def create_block(self):
        print("\nCreating a new block by Process of Leader Selection using Proof of Stake : ")
        maxStake = -1
        leadernode = {}
        for user in self.Users:
            stake = user['balance'] + user['security']
            if maxStake < stake:
                maxStake = stake
                leadernode = user
        for user in self.Users:       
            if leadernode['userId'] == user['userId']:
                user['reward'] += 100
        self.new_block(maxStake)
        print('Mined by: ', leadernode)

    def Reg_User(self):
        print('Enter User id: ')
        userId = input()
        print('Enter User name: ')
        userName = input()
        print('Enter your Password')
        password = input()
        print('Enter User Balance: ')
        balance = int(input())
        print('Enter Security Deposit: ')
        security = int(input())
        print('Enter Role: 1 if Distributor or 2 for Consumer ')
        role = int(input())
        while(role != 1 and role != 2):
            print('Enter Role: 1 if Distributor or 2 for Consumer ')
            role = int(input())
        #Check if user is already present
        for u in self.Users:
            if  u['userId'] == userId:
                print('User already present')
                return
        self.add_User(userId, userName, password, balance, security, role)

    def add_User(self, userId, userName, password, balance, security, role):
        User = {
            'userId' : userId,
            'userName': userName,
            'password' : password,
            'balance': balance,
            'security' : security,
            'role' : role,
            'reward' : 0
        }
        #signing the key for user verification
        msg= (userId + userName).encode()
        #Generating a random key as user's private key
        private_key = SigningKey.generate()
        #Corresponding companion key
        public_key = private_key.verifying_key
        #Signing the msg with user's private key
        sign = private_key.sign(msg)

        #validating the Node using public key
        if(self.validate_user(public_key, sign, userId, userName) is True):

            self.Users.append(User)
            #insert userId and balance in Bloackchain's dictionary object
            self.dict_obj[userId]=balance
            self.elapsedTime_dictobj[userId]=0

            print("\nNew Node details added.\n")
        else:
            print("Invalid node\n")
    
    def validate_user(self,public_key, signature, userId, userName):
        print("New Node is being validated before joining the other verified nodes...")
        #node verification
        msg=(userId + userName).encode()
        res = public_key.verify(signature, msg)
        print("Verified:", res )
        return res
    
    def Login(self):
        print('Enter User Id: ')
        userId = input()
        print('Enter your Password: ')
        password = input()
        for user in self.Users:
            if user['userId'] == userId and user['password'] == password:
                if user['role'] == 1:
                    self.dd(user)
                    return
                elif user['role'] == 2:
                    self.cd(user)
                    return
                elif user['role'] == 3:
                    self.md()
                    return
        print('Wrong Credentials')

    def dd(self,user):
        print('Distributor dashboard')
        d = int(input(('1:Delivery requests, 2:Dispatch a product, 3:Check Status, 4:Check Balance, 5:Exit\n')))
        while(d != 5):
            if(d == 1):
                self.delivery_request(user)
            elif(d == 2):
                self.dispatch_product(user)
            elif(d == 3):
                for i in self.Products:
                    if i['distributorId']==user['userId']:
                        self.generate_qr_code(i)
            elif(d == 4):
                print('Balance: ',user['balance'])  
            d = int(input(('1:Delivery requests, 2:Dispatch a product, 3:Check Status, 4:Check Balance, 5:Exit\n')))


    def cd(self,user):
        print('Client Dashboard')
        d = int(input(('1:Display Products, 2:Choose a Product, 3:Delivery Confirmation, 4:Check Status, 5:Check Balance, 6:Exit\n')))
        while(d != 6):
            if(d == 1):
                self.display_product()
            elif(d == 2):
                self.choose_product(user)
            elif(d == 3):
                self.delivery_confirmation(user)
            elif(d==4):
                for i in self.Products:
                    if i['clientId']==user['userId']:
                        self.generate_qr_code(i)
            elif(d==5):
                print('Balance: ',user['balance'])
            d = int(input(('1:Display Products, 2:Choose a Product, 3:Delivery Confirmation, 4:Check Status, 5:Check Balance, 6:Exit\n')))

    def md(self):
        print('Manufacturer Dashboard')
        c = int(input(('1:Add Product, 2:Display Products, 3:Exit\n')))
        while(c != 3):
            if(c == 1):
                self.add_product()
            elif(c == 2):
                self.display_products()
            c = int(input(('1:Add Product, 2:Display Products, 3:Exit\n')))

    def display_blockchain(self):
        print('\nBlocks: ')
        for i in self.chain:
            print(i)

    def add_product(self):
        productId = int(input('Enter Product Id: '))
        price = int(input('Enter the Price: '))
        product = {
            'productId' : productId,
            'price' : price,
            'clientId' : 0,
            'distributorId' : 0,
            'f1' : -1,
            'f2' : -1,
            'D_from_M':0,
            'D_dispatched':0,
            'C_recieved':0,
            'Delivered':0  
        }
        self.Products.append(product)
    
    def display_products(self):
        print('\nProducts: ')
        for i in self.Products:
            print(i)
    
    def display_product(self):
        print('Products: ')
        for i in self.Products:
            if i['clientId'] == 0:
                print('Product Id: ', i['productId'])
                print('Price: ', i['price'])

    def choose_product(self,user):
        while(True):
            f = int(input('Enter the Product Id: '))
            for i in self.Products:
                if i['productId'] == f:
                    if i['price'] > user['balance']:
                        print('Insufficient balance\n')
                        return
                    else:
                        i['clientId'] = user['userId']
                        i['order_time'] = time()
                        user['balance'] -= i['price']
                        return

    def delivery_request(self,user):       
        for i in self.Products:
            if i['distributorId'] == user['userId'] and i['Delivered'] == 0:
                print('You have Pending Delivery, cant take up more orders')
                return
        print('Requests: ')
        for i in self.Products:
            if i['clientId'] != 0 and i['Delivered'] == 0:
                i['D_from_M']=time()
                print('Product Id: ', i['productId'])
                print('Price: ', i['price'])
                print('Requested By: ', i['clientId'])
                
    def dispatch_product(self,user):
        for i in self.Products:
            if i['distributorId'] == user['userId'] and i['Delivered'] == 0:
                print('You have Pending Delivery, cant take up more orders')
                return      
        f = int(input('Enter the Product Id: '))
        for g in self.Products:
            if g['clientId'] == f:
                print('No one ordered this Product')
                return
        d = int(input(('1:Really disptach it, 2:Lie about dispatching, 3:Exit\n')))
        while(d!=3):
            if (d == 1):
                for i in self.Products:
                    if i['productId'] == f:
                        i['D_dispatched']=time()
                        i['f1'] = 0
                        i['distributorId'] = user['userId']
                        user['balance'] += i['price']
                        break
            elif (d == 2):
                for i in self.Products:
                    if i['productId'] == f:
                        i['D_dispatched']=time()
                        i['f1'] = 1
                        i['distributorId'] = user['userId']
                        break
            d = int(input(('1:Really disptach it, 2:Lie about dispatching, 3:Exit\n')))
    
    def delivery_confirmation(self,user):
        options = []
        die = int(input('Here are your products, choose one:'))
        for i in self.Products:
            if i['clientId'] == user['userId']:
                options.append(i['productId'])
                print(i['productId'])
        wp = int(input('Enter Product Id: '))
        if wp not in options:
            return
        for i in self.Products:
            if i['clientId'] == user['userId'] and i['productId'] == wp:
                if i['f1'] == -1:
                   print('Request not yet accepted')
                elif i['f1'] == 0:
                    i['C_received']=time()
                    d = int(input(('1:Acknowledge it correctly, 2:Acknowledge it incorrectly\n')))
                    if d == 1:
                        i['f2'] = 0
                        i['Delivered'] = 1
                        g = self.add_transaction(i)
                        self.complete_transactions.append(g)
                        print(g)
                        if len(self.complete_transactions) >= self.bf:
                            self.create_block()
                    elif d == 2:
                        i['f2']=1
                        i['Delivered'] = 1
                        user['security'] = int(0.9*user['security'])
                else:
                    for f in self.Users:
                        if f['userId'] == i['distributorId']:
                            f['security'] = int(0.9*f['security'])
                    g = int(input('1:Received, 2:Not Received'))
                    if g == 2:
                        print('Sorry for Inconvenience, refund will be initiated')
                        user['balance'] += i['price']                  
                break

    def add_transaction(self,i):
        Transaction = {
            'manufactureId': 1,
            'clientId': i['clientId'],
            'distributorId': i['distributorId'],
            'productId' : i['productId'],
            'price': i['price'],
            'Distributor (Di) got from the manufacturer': i['D_from_M'],
            'Distributor dispatched':i['D_dispatched'],
            'Client (Ci) received':i['C_received']
        }
        return Transaction
    
    def generate_qr_code(self,i):
        # Fetch product status from the blockchain (you would need to implement this)
        # For simplicity, assume the product status is represented as a boolean value.
        # You can customize this based on your actual data structure.
        

        # Create a text description of the product status
        status_text = f"Product ID: {i['productId']}\nDispatched: {'Yes' if i['f1']!=-1 else 'No'}\nReceived: {'Yes' if i['f2']==0 else 'No'}\n Status:{'Success ' if (i['f1']==0 and i['f2']==0) else 'Failed' }"

        # Generate a QR code with the status text
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(status_text)
        qr.make(fit=True)

        # Create an image from the QR code
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Save or display the QR code image
        qr_img.save(f"product_status_{i['productId']}.png")

    def chain_valid(self):
        #Starting with the genesis block
        previous_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            #Current block
            block = self.chain[block_index]
            #Recalulating the hash of the previous block and matching it with the previous block hash 
            if block['previous_hash'] != self.calculate_hash(previous_block):
                return False
            block_index += 1
            #Assigning the previous block variable to current block
            previous_block = block
        return True  


blockchain = BlockChain()
loop = 1
#timeLimit = 300
while(loop == 1):
    # ct = time()
    # for p in blockchain.Products:
    #     if p['clientId'] != 0 and p['distributorId'] != 0 and ct - p['D_dispatched'] >= timeLimit:
    print('\nEnter 1 for Registration, 2 to Login, 3 to View Blockchain, 4 to Verify Blockchain, 5 to exit')
    c = int(input())
    if(c == 5):
        loop = 0
    elif(c == 1):
        blockchain.Reg_User()
    elif(c == 2):
        blockchain.Login()
    elif(c == 3):
        blockchain.display_blockchain()
    elif(c == 4):
        k = blockchain.chain_valid()
        if k == True:
            print('Valid Blockchain')
        else:
            print('Blockchain is not valid')