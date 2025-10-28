from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestTransfers:

    def test_incoming_transfer(self):
        account = PersonalAccount("Bill", "Smith", "60010112345")
        account.incoming_transfer(100.0)

        assert account.balance == 100.0

    def test_outgoing_transfer(self):
        account = PersonalAccount("John", "Doe", "60010112345")
        account.balance = 200.0
        account.outgoing_transfer(50.0)
        
        assert account.balance == 150.0

    def test_transfer_insufficient_funds(self):
        account = PersonalAccount("Bill", "Smith", "60010112345")
        account.outgoing_transfer(30.0)

        assert account.balance == 0.0

    def test_transfer_negative_account(self):
        account = PersonalAccount("Anna", "Smith", "60010112345")
        account.incoming_transfer(-30.0)
        assert account.balance == 0.0

    # testy dla przelewow ekspresowych

    def test_express_transfer_personal(self):
        account = PersonalAccount("John", "Doe", "60010112345")
        account.balance = 200.0
        account.express_transfer(30)
        assert account.balance == 169

    def test_express_transfer_company(self):
        account = CompanyAccount("Firma", "123")
        account.balance = 200.0
        account.express_transfer(30)
        assert account.balance == 165

    def test_express_transfer_company_negative_balance(self):
        account = CompanyAccount("Firma", "123")
        account.balance = 30.0
        account.express_transfer(30)
        assert account.balance == -5

    def test_express_transfer_personal_negative_balance(self):
        account = PersonalAccount("John", "Doe", "60011123405")
        account.balance = 2.0
        account.express_transfer(3)
        assert account.balance == 2 # przelew nie przechodzi bo nie mozna miec na koncie mniej niz cena przelewu

    def test_express_transfer_zero_personal(self):
        account = PersonalAccount("John", "Doe", "60010112345")
        account.balance = 100
        account.express_transfer(0)
        assert account.balance == 100.0

    def test_express_transfer_negative_amount_company(self):
        account = CompanyAccount("Firma", "1234567890")
        account.balance = 100
        account.express_transfer(-50)
        assert account.balance == 100.0

    def test_express_transfer_not_enough_for_fee_personal(self):
        account = PersonalAccount("John", "Doe", "60010112345")
        account.balance = 0.5
        account.express_transfer(0.6)
        assert account.balance == 0.5

    def test_express_transfer_not_enough_for_fee_company(self):
        account = CompanyAccount("Firma", "1234567890")
        account.balance = 0.5
        account.express_transfer(0.6)
        assert account.balance == 0.5

