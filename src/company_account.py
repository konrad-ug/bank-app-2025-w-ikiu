from src.account import Account


class CompanyAccount(Account):
    def __init__(self, name, nip):
        self.name = name
        self.nip = nip if len(nip) == 10 and nip.isdigit() else "Invalid"