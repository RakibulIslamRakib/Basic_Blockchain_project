# Initializing our blockchain list:
genesis_block = {
           'previous_hash': '',
           'index': 0,
           'transactions': []
  }
blockchain = [genesis_block]
open_transactions = []
owner = 'Max'


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
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
    open_transactions.append(transaction)


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    block = {'previous_hash': hashed_block,
             'index': len(blockchain),
             'transactions': open_transactions
           }
    blockchain.append(block)


def get_transaction_value():

    """ Return the input of the user (A new transaction) as a float """
    tx_recipient = input("Enter the recipient of the transaction")
    tx_amount = float(input('your transaction amount please: '))
    return (tx_recipient, tx_amount)


def get_user_choice():
    user_input = input("your choice: ")
    return user_input


def print_blockchain_elements():
    # Output the blockchain list to the console
    for block in blockchain:
        print("Outtputing block:")
        print(block)
        print("_"*20)


def verify_chain():
    """varify the blockchain. Return true if valid otherwise return false"""
    for (index,block) in enumerate(blockchain):
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
    print("h: manipulate blockchain")
    print("q: quit")

    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient, amount = amount)
        print(open_transactions)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Chris','recipient': 'Max','amount':100}]
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


else:
    print("User Left!")
print("Done")
