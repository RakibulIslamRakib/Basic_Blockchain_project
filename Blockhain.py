# Initializing our blockchain list:

MINING_REWARD = 10
genesis_block = {
           'previous_hash': '',
           'index': 0,
           'transactions': []
  }
blockchain = [genesis_block]
open_transactions = []
owner = 'Max'
participants = {'Max'} #participants contains all unique sender and recipants


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount =1.0):
    """
        sender: the sender of the coins.
        receiver: the recipient of the coins.
        ammount: The amount of coins sent with transaction (default value =1.0)
    """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_recieved = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_recieved += tx[0]
    return amount_recieved - amount_sent


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction={
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    copied_transaction = open_transactions[:]
    copied_transaction.append(reward_transaction)
    block = {'previous_hash': hashed_block,
             'index': len(blockchain),
             'transactions': copied_transaction
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
    return True


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
            open_transactions=[]
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)

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
    print(get_balance('Max'))


else:
    print("User Left!")
print("Done")