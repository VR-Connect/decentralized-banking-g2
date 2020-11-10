from flask import Flask
import json
import requests

class Account:
    def __init__(self, adress):
        self.adress = adress
        self.balance = 0

    def show_balance(self):
        return str(self.balance)

    def __eq__(self, other):
        if self.adress == other.adress:
            return True
        return False

    def transaction(self, amount):
        self.balance += amount
        return True

    def representaion(self):
        return {
            "adress" : self.adress,
            "amount" : self.balance
        }

class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, adress):
        input = requests.post('http://195.201.87.110:5000/'+ adress)
        print(input)

        newacc= Account(adress)
        if(newacc.adress in self.accounts.keys()):
            # account already exists
            return False
        self.accounts[adress] = newacc
        return True

    def handle_transaction(self, sender, receiver, amount):
        if sender not in self.accounts.keys() or receiver not in self.accounts.keys():
            return False
        self.accounts[sender].transaction(-amount)
        self.accounts[receiver].transaction(amount)
        return True

    def show_accounts(self):
        return [acc.representaion() for acc in self.accounts.values()]

    def show_account(self, adress):
        if adress not in self.accounts.keys():
            return False
        return self.accounts[adress].show_balance()

    def check(self, adress):
        if adress not in self.accounts.keys():
            return False
        return True

app = Flask(__name__)

global bank
bank = Bank()

@app.route('/', methods=['GET'])
def show_accounts():
    return json.dumps(bank.show_accounts())

@app.route('/<adress>', methods=['POST'])
def create_account(adress):
    if bank.create_account(str(adress)):
        return "New Account created", 200
    return 'Account already exists', 401

@app.route('/<sender>/<receiver>/<amount>', methods=['POST'])
def transfer(sender, receiver, amount):
    sender = str(sender)
    receiver = str(receiver)
    amount = int(amount)
    if bank.handle_transaction(sender, receiver, amount):
        return 'Transaktion Successful', 200
    return 'ERROR', 401

@app.route('/<adress>', methods=['GET'])
def show_amount(adress):
    if bank.check(adress):
        return bank.show_account(adress), 200
    return 'Invalid account', 401

if __name__ == '__main__':
 app.run(debug=True, host='0.0.0.0', port='80')

