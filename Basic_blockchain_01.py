# Initializing our blockchain list:
blockchain=[]


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(transaction_amount, last_transaction=[1]):
    """
        Append a new value as well as the last value to the blockchain

        pasameters:
            transaction_amount: the amount that should be added.
            last_transaction:The last blockchain transaction(default[1])
    """
    if last_transaction is None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_value():
    """ Return the input of the user (A new transaction) as a float """
    user_input=float(input('your transaction amount please: '))
    return user_input


def get_user_choice():
    user_input=input("your choice: ")
    return user_input


def print_blockchain_elements():
    # Output the blockchain list to the console
    for block in blockchain:
        print("Outtputing block:")
        print(block)
        print("_"*20)


def varify_chain():
    #block_index = 0
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index-1]:
            is_valid = True
        else:
            is_valid = False

    """
      for block in blockchain:
        if block_index == 0:
            block_index += 1
            continue
        elif block[0] == blockchain[block_index-1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1  
    """
    return is_valid


waiting_for_input = True

while waiting_for_input:
    print("please enter your choice:")
    print("1: Add a new transaction value")
    print("2: Output the blockchain blocks")
    print("h: manipulate blockchain")
    print("q: quit")

    user_choice = get_user_choice()
    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]

    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print("Input was invalid. Please pick a value from the list!")
    print("Choice registered!")
    if not varify_chain():
        print_blockchain_elements()
        print("Invalid blockchain")
        break

else:
    print("User Left!")
print("Done")
