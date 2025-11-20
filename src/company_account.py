from src.account import Account

class CompanyAccount(Account):
    def __init__(self, name, nip):
        super().__init__(name, "")
        self.name = name
        self.nip = nip if len(nip) == 10 and nip.isdigit() else "Invalid"

    def express_transfer(self, amount):
        express_transfer_fee = 5.0
        total = amount + express_transfer_fee

        if amount > 0 and self.balance and (self.balance - total) >= express_transfer_fee*(-1):
            self.balance -= (amount + express_transfer_fee)

            self.transfer_history.append(amount*(-1))
            self.transfer_history.append(express_transfer_fee*(-1))

            return True
        return False
    
    def take_loan(self, amount):
        if self._is_twice_as_big(amount) and self._zus_transfer_exists():
            self.balance += amount
            return True
        return False

    def _is_twice_as_big(self, amount):
        if amount*2 <= self.balance:
            return True
        return False
    
    def _zus_transfer_exists(self):
        if -1775 in self.transfer_history:
            return True
        else:
            return False