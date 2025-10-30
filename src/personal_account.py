from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        super().__init__(first_name, last_name)
        self.first_name = first_name
        self.last_name = last_name

        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"

        self.balance = 50 if self.can_get_promo(pesel) and self.is_promo_code_valid(promo_code) else 0.0

    def is_pesel_valid(self, pesel):
        return isinstance(pesel, str) and len(pesel) == 11
    
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
            return True
        return False

