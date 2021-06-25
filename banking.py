from random import randint
import sqlite3

account_numbers = []
account = ()
pin = ()
customer_balance = 0
checksum = ()
full_account = ()
conn = sqlite3.connect('card.s3db')
c = conn.cursor()


def create_table():
    c.execute('''DROP TABLE IF EXISTS card''')
    conn.commit()
    c.execute('''CREATE TABLE IF NOT EXISTS card
                 (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER)''')
    conn.commit()


def entry_menu():
    choice = input("1. Create an account\n2. Log into account\n0. Exit\n")
    if choice == "0":
        stop()
    elif choice == "1":
        create_account()
    elif choice == "2":
        log_in()


def account_menu():
    choice = ()
    while choice != 0:
        choice = int(input(("1. Balance\n2. Add income\n3. Do transfer\n"
                            "4. Close account\n5. Log out\n0. Exit\n")))
        if choice == 1:
            check_balance()
        elif choice == 2:
            add_income()
        elif choice == 3:
            transfer_money()
        elif choice == 4:
            close_account()
        elif choice == 5:
            print("\nYou have successfully logged out!\n")
            entry_menu()
    stop()


def create_account():
    global account
    account = ()
    generate_account()
    print("Your card has been created")
    print("Your card number:")
    print(str(full_account))
    generate_pin()
    print("Your card PIN:")
    print(str(pin) + "\n")
    add_customer()
    entry_menu()


def generate_account():
    global account
    global full_account
    global checksum
    random_list = []
    account = ()
    i = 1
    while i <= 9:
        n = randint(0, 9)
        random_list.append(str(n))
        i += 1
    account = "".join(random_list)
    if account not in account_numbers:
        checksum = randint(1, 9)
        full_account = "400000" + str(account) + str(checksum)
        if check_luhn(full_account) is True:
            account_numbers.append(account)
        else:
            generate_account()
    else:
        generate_account()


def check_luhn(number):
    ndigits = len(number)
    nsum = 0
    issecond = False
    for i in range(ndigits - 1, -1, -1):
        d = ord(number[i]) - ord('0')
        if issecond:
            d = d * 2
        nsum += d // 10
        nsum += d % 10
        issecond = not issecond
    if nsum % 10 == 0:
        return True
    else:
        return False


def generate_pin():
    global pin
    pin = ()
    n = randint(1000, 9999)
    pin = str(n)


def add_customer():
    c.execute('''INSERT INTO card (number, pin, balance) VALUES (?, ?, 0)''',
              (full_account, pin))
    conn.commit()


def log_in():
    global customer_balance
    global full_account
    print("\nEnter your card number:")
    input_number = input()
    print("Enter your PIN:")
    input_pin = input()
    c.execute('''SELECT * FROM card WHERE number = ? AND pin = ?''',
              (input_number, input_pin))
    if len(list(c)) != 0:
        c.execute('''SELECT * FROM card WHERE number = ? AND pin = ?''',
                  (input_number, input_pin))
        print("\nYou have successfully logged in!\n")
        customer_balance = c.fetchone()[3]
        full_account = input_number
        account_menu()
    else:
        print("\nWrong card number or PIN!\n")
        entry_menu()


def check_balance():
    global full_account
    c.execute('''SELECT balance FROM card WHERE number = ?''', (full_account,))
    print('\nBalance: ' + str(c.fetchone()[0]) + "\n")


def add_income():
    global customer_balance
    global full_account
    income = int(input("\nEnter income:\n"))
    customer_balance += income
    c.execute('''UPDATE card set balance = ? WHERE number = ?''', (customer_balance, str(full_account)))
    conn.commit()
    print("Income was added!\n")
    account_menu()


def transfer_money():
    global customer_balance
    transfer_card = int((input("\nTransfer\nEnter card number: \n")))
    if check_luhn(str(transfer_card)) is True:
        if str(transfer_card) != full_account:
            c.execute('''SELECT * FROM card WHERE number = ?''', (str(transfer_card),))
            if len(list(c)) > 0:
                transfer = int(input("Enter how much money you want to transfer:\n"))
                if transfer > customer_balance:
                    print("Not enough money!\n")
                    account_menu()
                else:
                    c.execute('''SELECT * FROM card WHERE number = ?''', (str(transfer_card),))
                    transfer_balance = c.fetchone()[3]
                    c.execute('''UPDATE card SET balance = ? WHERE number = ?''',
                              ((transfer + transfer_balance), transfer_card))
                    conn.commit()
                    c.execute('''UPDATE card SET balance = ? WHERE number = ?''',
                              ((customer_balance - transfer), full_account))
                    conn.commit()
                    customer_balance -= transfer_balance
                    print("Success!\n")
            else:
                print("Such a card does not exist.")
                account_menu()
        else:
            print("You can't transfer money to the same account!\n")
    else:
        print("Probably you made a mistake in the card number. "
              "Please try again!\n")
        account_menu()


def close_account():
    c.execute('''DELETE FROM card where number = ?''', (full_account,))
    conn.commit()
    print("\nThe account has been closed!\n")


def stop():
    print("\nBye!")
    exit()


create_table()
entry_menu()
