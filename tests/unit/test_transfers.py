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
        # account.incoming_transfer(200.0)
        
        assert account.balance == 150.0

    def test_transfer_insufficient_funds(self):
        account = PersonalAccount("Bill", "Smith", "60010112345")
        account.outgoing_transfer(30.0)

        assert account.balance == 0.0

    def test_transfer_negative_account(self):
        account = PersonalAccount("Anna", "Smith", "60010112345")
        account.incoming_transfer(-30.0)
        assert account.balance == 0.0
