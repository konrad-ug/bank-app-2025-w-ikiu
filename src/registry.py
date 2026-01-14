from src.personal_account import PersonalAccount

class AccountsRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account: PersonalAccount):
        # sprawdzenie czy pesel istnieje
        if self.get_account_by_pesel(account.pesel):
            return False
        self.accounts.append(account)
        return True

    def number_of_accounts(self):
        return len(self.accounts)

    def get_account_by_pesel(self, pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None
    
    def get_all_accounts(self):
        return self.accounts

    # usuwanie do feature 15
    def delete_account(self, pesel):
        account = self.get_account_by_pesel(pesel)
        if account:
            self.accounts.remove(account)
            return True
        return False
    
    def cleanup(self):
        self.accounts = []