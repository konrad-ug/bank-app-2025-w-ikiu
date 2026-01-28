from src.account import Account
from datetime import date

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None, balance=None):
        super().__init__(first_name, last_name)
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.transfer_history = []

        if balance is not None:
            self.balance = float(balance)
        else:
            self.balance = 50 if self.can_get_promo(pesel) and self.is_promo_code_valid(promo_code) else 0.0

    def is_pesel_valid(self, pesel):
        return isinstance(pesel, str) and len(pesel) == 11
    
    # do feature 19
    def send_history_via_email(self, to_email, smtp_client):
        today = date.today()
        subject = f"Account Transfer History {today}"
        
        body = f"Personal account history: {self.transfer_history}"
        
        return smtp_client.send(subject, body, to_email)
    
    def is_promo_code_valid(self, promo_code):
        return isinstance(promo_code, str) and promo_code.startswith("PROM_") and len(promo_code) == 8
    
    def can_get_promo(self, pesel):
        if not self.is_pesel_valid(pesel):
            return False
        yy, mm = int(pesel[:2]), int(pesel[2:4])
        if 1 <= mm <= 12:
            year = 1900 + yy
        elif 21 <= mm <= 32:
            year = 2000 + yy
        else:
            return False
        return year > 1960
    
    def express_transfer(self, amount):
        express_transfer_fee = 1.0
        total = amount + express_transfer_fee
        
        if amount > 0 and (self.balance - total) >= express_transfer_fee*(-1):
            self.balance -= (amount + express_transfer_fee)

            self.transfer_history.append(amount*(-1))
            self.transfer_history.append(express_transfer_fee*(-1))
            return True
        return False
    
    def submit_for_loan(self, amount):
        if self._check_last_three_positive() or self._check_sum_greater_than_loan(amount):
            self.balance += amount
            return True
        return False
    
    def _check_last_three_positive(self):
        if len(self.transfer_history) < 3:
            return False
        return all(t > 0 for t in self.transfer_history[-3:])

    def _check_sum_greater_than_loan(self, amount):
        if len(self.transfer_history) < 5:
            return False
        return sum(self.transfer_history[-5:]) > amount
    
    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "pesel": self.pesel,
            "balance": self.balance,
            "history": self.transfer_history
        }