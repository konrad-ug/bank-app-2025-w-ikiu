class Account:
    def __init__(self, first_name, last_name):
        self.balance = 0.0
        self.transfer_history = []

    def incoming_transfer(self, amount):
        if amount <= 0:
            return False
        self.balance += amount

        self.transfer_history.append(amount)
        return True

    def outgoing_transfer(self, amount):
        if amount > self.balance:
            self.balance
            return False
        else:
            self.balance -= amount
            negative_amount = amount*(-1)
            self.transfer_history.append(negative_amount)
            return True

    # def no_tests_method(self): 
    #     return 4
