from src.account import Account
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestHistory:
    # konto osobiste
    def test_history_after_transfers_personal(self):
        account = PersonalAccount("John", "Doe", "12345678900")
        account.incoming_transfer(500)
        account.outgoing_transfer(300)
        assert account.balance == 200.0
        assert account.transfer_history == [500, -300]

    def test_history_after_transfers_not_enough_money_personal(self):
        account = PersonalAccount("John", "Doe", "12345678900")
        account.incoming_transfer(300)
        account.outgoing_transfer(500)
        assert account.balance == 300.0
        assert account.transfer_history == [300]

    def test_history_after_many_transfers_personal(self):
        account = PersonalAccount("John", "Doe", "12345678900")
        account.incoming_transfer(500)
        account.outgoing_transfer(300)
        account.outgoing_transfer(50)
        account.incoming_transfer(100)
        assert account.balance == 250.0
        assert account.transfer_history == [500, -300, -50, 100]

    # konto firmowe
    def test_history_after_transfers_company(self):
        account = CompanyAccount("Firma", "1234567890")
        account.incoming_transfer(500)
        account.outgoing_transfer(300)
        assert account.balance == 200.0
        assert account.transfer_history == [500, -300]

    def test_history_after_transfers_not_enough_money_company(self):
        account = CompanyAccount("Firma", "1234567890")
        account.incoming_transfer(300)
        account.outgoing_transfer(500)
        assert account.balance == 300.0
        assert account.transfer_history == [300]

    def test_history_after_many_transfers_company(self):
        account = CompanyAccount("Firma", "1234567890")
        account.incoming_transfer(500)
        account.outgoing_transfer(300)
        account.outgoing_transfer(50)
        account.incoming_transfer(100)
        assert account.balance == 250.0
        assert account.transfer_history == [500, -300, -50, 100]

    # przelewy ekspresowe

    # konto osobiste
    def test_express_personal(self):
        account = PersonalAccount("John", "Doe", "12345678900")
        account.balance = 500.0
        account.express_transfer(50)
        assert account.balance == 449.0
        assert account.transfer_history == [-50, -1]

    def test_express_personal_2(self):
        account = PersonalAccount("John", "Doe", "12345678900")
        account.incoming_transfer(500)
        account.express_transfer(50)
        assert account.balance == 449.0
        assert account.transfer_history == [500, -50, -1]

    def test_express_personal_not_enough_money(self):
        account = PersonalAccount("John", "Doe", "12345678900")
        account.balance = 10.0
        account.express_transfer(50)
        assert account.balance == 10.0
        assert account.transfer_history == []

    def test_express_personal_invalid_amount(self):
        account = PersonalAccount("John", "Doe", "12345678900")
        account.balance = 500.0
        account.express_transfer(0)
        assert account.transfer_history == []

    def test_express_personal_minus_balance(self):
        account = PersonalAccount("John", "Doe", "12345678900")
        account.incoming_transfer(3)
        account.express_transfer(3)
        assert account.balance == -1
        assert account.transfer_history == [3, -3, -1]

    # konto firmowe
    def test_express_company(self):
        account = CompanyAccount("Firma1", "1234567890")
        account.balance = 500.0
        account.express_transfer(50)
        assert account.balance == 445.0
        assert account.transfer_history == [-50, -5]

    def test_express_company_2(self):
        account = CompanyAccount("Firma1", "1234567890")
        account.incoming_transfer(500)
        account.express_transfer(50)
        assert account.balance == 445.0
        assert account.transfer_history == [500, -50, -5]

    def test_express_company_not_enough_money(self):
        account =CompanyAccount("Firma1", "1234567890")
        account.balance = 10.0
        account.express_transfer(50)
        assert account.balance == 10.0
        assert account.transfer_history == []

    def test_express_company_minus_balance(self):
        account =CompanyAccount("Firma1", "1234567890")
        account.incoming_transfer(10)
        account.express_transfer(10)
        assert account.balance == -5
        assert account.transfer_history == [10, -10, -5]