from functools import reduce
from hashlib import sha256
from collections import OrderedDict
import json
from hash_util import hash_string_256, hash_block

# Initializing our blockchain list:

MINING_REWARD = 10
genesis_block = {
           'previous_hash': '',
           'index': 0,
           'transactions': [],
           'proof' : 100
  }
blockchain = [genesis_block]
open_transactions = []
owner = 'Max'
participants = {'Max'} #participants contains all unique sender and recipants


def load_data():
    with open('blockchain.txt',mode='r')as f:
        file_content = f.readlines()
        global blockchain
        global open_transactions
        blockchain = json.loads(file_content[0][:-1])
        updated_blockchain = []
        for block in blockchain:
            updated_block = {
                'previous_hash': block['previous_hash'],
                'index': block['index'],
                'proof': block['proof'],
                'transactions': [OrderedDict(
                    [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]) for tx in block['transactions']]
            }
            updated_blockchain.append(updated_block)
        blockchain = updated_blockchain

        open_transactions = json.loads(file_content[1])
        updated_transactions = []
        for tx in open_transactions:
            updated_transaction = OrderedDict(
                    [('sender',tx['sender']),('recipient',tx['recipient']),('amount',tx['amount'])])
            updated_transactions.append(updated_transaction)
        open_transactions = updated_transactions


load_data()


def save_data():
    with open('blockchain.txt',mode='w') as f:
        f.write(json.dumps(blockchain))
        f.write('\n')
        f.write(json.dumps(open_transactions))


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount = 1.0):
    """
        sender: the sender of the coins.
        receiver: the recipient of the coins.
        ammount: The amount of coins sent with transaction (default value =1.0)
    """
    #transaction = {
     #   'sender': sender,
      #  'recipient': recipient,
       # 'amount': amount
    #}
    transaction = OrderedDict([('sender', sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hashed = hash_string_256(guess)
    print(guess_hashed)
    return guess_hashed[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions
                      if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amm: tx_sum + sum(tx_amm) if len(tx_amm) > 0 else tx_sum + 0, tx_sender, 0)

    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amm: tx_sum + sum(tx_amm) if len(tx_amm) > 0 else tx_sum + 0, tx_recipient, 0)
    return amount_received - amount_sent


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()

    #reward_transaction={
     #   'sender': 'MINING',
      #  'recipient': owner,
       # 'amount': MINING_REWARD
    #}

    reward_transaction = OrderedDict(
        [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
    copied_transaction = open_transactions[:]
    copied_transaction.append(reward_transaction)
    block = {'previous_hash': hashed_block,
             'index': len(blockchain),
             'transactions': copied_transaction,
             'proof': proof
           }
    blockchain.append(block)
    return True


def get_transaction_value():

    """ Return the input of the user (A new transaction) as a float """
    tx_recipient = input("Enter the recipient of the transaction : ")
    tx_amount = float(input('your transaction amount please : '))
    return tx_recipient, tx_amount


def get_user_choice():
    user_input = input("your choice : ")
    return user_input


def print_blockchain_elements():
    # Output the blockchain list to the console
    for block in blockchain:
        print("Outputting block:")
        print(block)
        print("_"*20)


def verify_chain():
    """verify the blockchain. Return true if valid otherwise return false"""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
        if not valid_proof(block['transactions'][:-1],block['previous_hash'],block['proof']):
            print('proof of work is invalid')
            return False

    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True

while waiting_for_input:
    print("please enter your choice:")
    print("1: Add a new transaction value")
    print("2: Mine a new block")
    print('3: Output the blockchain blocks')
    print('4: Output the participants')
    print('5: check transaction validity')
    print("h: manipulate blockchain")
    print("q: quit")

    user_choice = get_user_choice()
    if user_choice == '1':
        recipient, amount = get_transaction_value()
        #add transaction amount to the blockchain
        if add_transaction(recipient, amount=amount):
            print('Added transaction!')
        else:
            print('Transaction Failed')

        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are velid')
        else:
            print('Therre are invelid transaction')
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Chris', 'recipient': 'Max', 'amount': 100}]
            }

    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print("Input was invalid. Please pick a value from the list!")
    print("Choice registered!")
    if not verify_chain():
        print_blockchain_elements()
        print("Invalid blockchain")
        break
    print('Balance of {} : {:6.2f}'.format('Max',get_balance('Max')))


else:
    print('user left')