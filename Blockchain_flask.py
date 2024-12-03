import hashlib
import json
from time import time
from flask import Flask, jsonify, request

# Blockchain class
class Block_Chain:
    def __init__(self):
        self.chain = []
        self.pendingTransactions = []
        # Genesis block
        self.newBlock(previousHash="This is Reehan and the date is Dec/04/2024", proof=100)

    def newBlock(self, proof, previousHash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pendingTransactions,
            'proof': proof,
            'previous_hash': previousHash or self.hash(self.chain[-1]) if self.chain else None,
        }
        self.pendingTransactions = []
        self.chain.append(block)
        return block

    def hash(self, block):
        blockString = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(blockString).hexdigest()

    def lastBlock(self):
        return self.chain[-1] if self.chain else None

    def newTransaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        }
        self.pendingTransactions.append(transaction)
        return self.lastBlock()['index'] + 1 if self.lastBlock() else 1

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            # Check if previous_hash is valid
            if block['previous_hash'] != self.hash(previous_block):
                return False

            # Check proof of work
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False

            previous_block = block
            block_index += 1

        return True

# Blockchain and Flask initialization (same as above)
blockchain = Block_Chain()
app = Flask(__name__)

# Add a new transaction
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    transaction_data = request.get_json()  # Get the transaction data from the POST request
    required_fields = ['sender', 'recipient', 'amount']

    # Check if all required fields are present
    if not all(field in transaction_data for field in required_fields):
        return jsonify({'message': 'Invalid transaction data. Required fields: sender, recipient, amount.'}), 400

    # Add the transaction
    index = blockchain.newTransaction(
        transaction_data['sender'],
        transaction_data['recipient'],
        transaction_data['amount']
    )

    response = {
        'message': f'Transaction will be added to Block {index}.',
        'transaction': transaction_data
    }
    return jsonify(response), 201

# Mine a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.lastBlock()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.newBlock(proof, previous_hash)

    response = {
        'message': 'A block is mined!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

# Display blockchain
@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

# Check blockchain validity
@app.route('/valid', methods=['GET'])
def valid():
    is_valid = blockchain.chain_valid(blockchain.chain)
    response = {'message': 'The Blockchain is valid.'} if is_valid else {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200

# Run the server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
