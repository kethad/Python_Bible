#Bank Account

class Account:
    def __init__(self, name, balance, min_balance):
        self.name = name
        self.balance = balance
        self.min_balance = min_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance - amount >= self.min_balance:
            self.balance -= amount
        else:
            print "Not enough funds!"

    def statement(self):
        print "Account Balance: RS{}".format(self.balance)

class Current(Account):
    def __init__(self, name, balance):
        super().__init__(name, balance, min_balance = -1000)

    def __str__(self):
        return "{}'s Current Account: Balance RS{}".format(self.name, self.balance)

class Savings(Account):
    def __init__(self, name, balance):
        Account.__init__(self, name, balance, min_balance = 0)
    def __str__(self):
        return "{}'s Saving Account: Balance RS{}".format(self.name, self.balance)



