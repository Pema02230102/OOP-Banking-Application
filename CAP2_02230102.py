#############################################################################
#############################################################################
#Pema Tshering
#1ECE
#02230102
#############################################################################
#############################################################################
#REFERENCES
#https://codereview.stackexchange.com/questions/236120/oop-banking-system
#https://www.geeksforgeeks.org/python-program-to-create-bankaccount-class-with-deposit-withdraw-function/
#https://codereview.stackexchange.com/questions/214886/oop-bank-account-program-in-python-3
#############################################################################
#############################################################################



import os      # Firstly, imported os module to interact with operating system.
import json    # Then json module is imported to convert data into json format and vice versa.   
import random   # random module is imported to generate random numbers.

class Account:   # Defined the class as Account to represent each bank account. 
    def __init__(self, acc_no, passw, acc_typ, bal=0):
     # Initialized the object "Account" with an account number, password, account type and an initial balance which the default is zero. 
        self.acc_no = acc_no
        self.passw = passw
        self.acc_typ = acc_typ
        self.bal = bal

    def deposit(self, amount):   # This method adds a specified amount to an account balance.
        self.bal += amount

    def withdr(self, amount):   # This method deducts a specified amount from the account balance if the funds are sufficient,
        if amount > self.bal:
            raise ValueError("Limited funds")   # and raises an valueerror if it is insufficient.
        self.bal -= amount

    def transfer(self, amount, tar_acc):  # This method transfers a specified amount to another account from the current account.
        self.withdr(amount)
        tar_acc.deposit(amount)

def create_account(acc_typ):
# Defined the function create_account to open a new account with random password and account number, saves it, and returns account details. 
    
    acc_no = str(random.randint(1000, 9999))
    passw = str(random.randint(100, 999))
    account = Account(acc_no, passw, acc_typ)
    save_account(account)
    return acc_no, passw

def save_account(account):    # The defined function saves account details to accounts.txt file.
    account_data = {
        "acc_no": account.acc_no,
        "passw": account.passw,
        "acc_typ": account.acc_typ,
        "bal": account.bal
    }
    with open("accounts.txt", "a") as f:
        f.write(json.dumps(account_data) + "\n")

def load_accounts():    # Function loads all accounts stored in the account file into a list of "Account"
    accounts = []
    if os.path.exists("accounts.txt"):
        with open("accounts.txt", "r") as f:
            for line in f:
                account_data = json.loads(line.strip())
                accounts.append(Account(**account_data))
    return accounts

def login(acc_no, passw):
# This function checks if an account with the given account_number and password exists or not.
# and returns account if it is found, otherwise returns None.

    accounts = load_accounts()
    for account in accounts:
        if account.acc_no == acc_no and account.passw == passw:
            return account
    return None

def update_accounts(account):
# # This function updates an account's information in the file.
# It reloads all accounts, replaces the modified account, and rewrites the file with updated data.

    accounts = load_accounts()
    for i, acc in enumerate(accounts):
        if acc.acc_no == account.acc_no:
            accounts[i] = account
            break
    with open("accounts.txt", "w") as f:
        for acc in accounts:
            account_data = {
                "acc_no": acc.acc_no,
                "passw": acc.passw,
                "acc_typ": acc.acc_typ,
                "bal": acc.bal
            }
            f.write(json.dumps(account_data) + "\n")

def delete_account(acc_no):
# This function deletes an account by loading all accounts and removing the account with specified acccount_number.
# and updates the accounts file with remaining accounts.

    accounts = load_accounts()
    accounts = [account for account in accounts if account.acc_no != acc_no]
    with open("accounts.txt", "w") as f:
        for account in accounts:
            account_data = {
                "acc_no": account.acc_no,
                "passw": account.passw,
                "acc_typ": account.acc_typ,
                "bal": account.bal
            }
            f.write(json.dumps(account_data) + "\n")

def transfer_money(from_account, to_acc_no, amount):
# This function tranfers money between accounts by,
# loading through all accounts and finding the target account.
# Raises an error if the target account does not exist and
# If target account founds, then transfer the amount and updates the account file.

    accounts = load_accounts()
    to_account = next((acc for acc in accounts if acc.acc_no == to_acc_no), None)
    if to_account is None:
        raise ValueError("No Account")
    from_account.transfer(amount, to_account)
    update_accounts(from_account)
    update_accounts(to_account)




def main():
#  This function provides the user interface, displaying options to open an account, log in, or exit.
    while True:
        print("\nBanking System")
        print("1. Open an Account")
        print("2. Login")
        print("3. Exit")
        ch = input("Select your choice: ")

        if ch == "1":
        # If the user chooses to open an account and 
        # they specify the account type, a new account is created and displayed.

            acc_typ = input("Select account type (Personal/Business): ")
            acc_no, passw = create_account(acc_typ)
            print(f" Successfully created Bank Account with Account Number: {acc_no}, Password: {passw}")

        elif ch == "2":
        # If the user chooses to log in and enter their credentials,
        # they are presented with further options for account management if valid.

            acc_no = input("Enter account number: ")
            passw = input("Enter password: ")
            account = login(acc_no, passw)
            if account:
                while True:
                    print("\n1. Check Balance")
                    print("2. Deposit Money")
                    print("3. Withdraw Money")
                    print("4. Transfer Money")
                    print("5. Delete Account")
                    print("6. Logout")
                    sub_ch = input("Select your choice: ")
                    

                    # The sub-menu options allow users to check their balance, deposit, withdraw, 
                    # transfer money, delete their account, or log out.
                    # Each action updates the account and saves changes to the file.
                    # It gives error if login fails.
                    
                    if sub_ch == "1":
                        print(f"Your Current balance is: {account.bal}")

                    elif sub_ch == "2":
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                        update_accounts(account)
                        print(f"Deposited {amount}. Your New balance is: {account.bal}")

                    elif sub_ch == "3":
                        amount = float(input("Enter amount to withdraw: "))
                        try:
                            account.withdr(amount)
                            update_accounts(account)
                            print(f"Withdrew {amount}. Your New balance is: {account.bal}")
                        except ValueError as e:
                            print(e)

                    elif sub_ch == "4":
                        to_acc_no = input("Enter target account number: ")
                        amount = float(input("Enter amount to transfer: "))
                        try:
                            transfer_money(account, to_acc_no, amount)
                            print(f"Transferred {amount} to account {to_acc_no}. Your New balance is: {account.bal}")
                        except ValueError as e:
                            print(e)

                    elif sub_ch == "5":
                        delete_account(account.acc_no)
                        print("Successfully deleted the account.")
                        break

                    elif sub_ch == "6":
                        break
                    else:
                        print("Wrong choice. Please try again.")

            else:
                print("Wrong account number or password.")

        elif ch == "3":
            print("Thanks for using the banking system.")
            break

        else:
            print("Wrong choice. Please try again.")

if __name__ == "__main__":
    main()
