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