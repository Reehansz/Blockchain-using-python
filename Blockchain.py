import hashlib
import json
from time import time

#creating the block_chain class

class Block_Chain(object):
    def __init__(self):
        self.chain = []
        self.pendingTransactions = []
        # self.newBlock(previousHash) = "The Times 03/Jan/2009 chancellor on brink of second bailout for banks.",proof = 100)
    
    def newBlock(self, the_proof):
        the_block = {
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'transactions' : self.pendingTransactions,
            'proof' : the_proof,
            'previous_hash' : self.hash()
        }
        self.pendingTransactions = []
        self.chain.append(the_block)
        return the_block
    
    def hash(self):
        if len(self.chain) > 0:
            block = self.chain[-1]
        else :
            return "This is Reehan date Dec/03/2024"
        blockString = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(blockString).hexdigest()

    def lastBlock(self):
        if len(self.chain)>0:
            return self.chain[-1] 
        else:
            return None
    
    def newTransaction(self, the_sender, the_recipient, the_amount):
        the_transaction = {
            'sender' : the_sender,
            'recipient' : the_recipient,
            'amount' : the_amount
        }
        self.pendingTransactions.append(the_transaction)
        return self.lastBlock()
   
block_chain = Block_Chain()
t1 = block_chain.newTransaction("Sathoshi", "Alex", '10 BTC')
t2 = block_chain.newTransaction("Alex", "Sathoshi", '2 BTC')
t3 = block_chain.newTransaction("Sathoshi", "James", '10 BTC')

block_chain.newBlock(10123)

t4 = block_chain.newTransaction("Lucy", "Alex", '2 BTC')
t5 = block_chain.newTransaction("Justin", "Lucy", '1 BTC')
t6 = block_chain.newTransaction("Lucy", "Alex", '1 BTC')

block_chain.newBlock(10384)

t7 = block_chain.newTransaction("Lucy", "Sathoshi", '2 BTC')
t8 = block_chain.newTransaction("Sathoshi", "Lucy", '1 BTC')
t9 = block_chain.newTransaction("Alex", "Sathoshi", '1 BTC')

block_chain.newBlock(10341)
print("Genisis block : ", block_chain.chain)
