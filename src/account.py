class Account:
    def __init__(self, first_name, last_name):
        self.balance = 0.0

    def incoming_transfer(self, amount):
        if amount <= 0:
            return False
        self.balance += amount
        return

    def outgoing_transfer(self, amount):
        if amount > self.balance:
            return self.balance
        else:
            self.balance -= amount
