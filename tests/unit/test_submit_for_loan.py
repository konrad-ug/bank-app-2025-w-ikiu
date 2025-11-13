from src.account import Account
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestLoan:
    def test_submit_for_loan_positive(self):
        account = PersonalAccount("John", "Doe", "12345678900")
        account.incoming_transfer(500)
        account.outgoing_transfer(300)
        account.incoming_transfer(200)
        account.incoming_transfer(400)
        account.incoming_transfer(2100)
        account.incoming_transfer(250)
        assert account.submit_for_loan(200) == True
        assert account.balance == 3350     

    def test_submit_for_loan_0_transfers(self):
        account = PersonalAccount("John", "Doe", "12345678900")
        assert account.submit_for_loan(200) == False
        assert account.balance == 0

    def test_submit_for_loan_no_3_last_positive_transfers(self):
        account = PersonalAccount("John", "Doe", "12345678900")
        account.incoming_transfer(500)
        account.incoming_transfer(300)
        account.incoming_transfer(200)
        account.outgoing_transfer(100)
        account.outgoing_transfer(100)
        account.outgoing_transfer(250)
        assert account.submit_for_loan(200) == False
        assert account.balance == 550

    def test_submit_for_loan_express_transfers(self):
        account = PersonalAccount("John", "Doe", "12345678900")
        account.incoming_transfer(500)
        account.incoming_transfer(300)
        account.incoming_transfer(200)
        account.outgoing_transfer(100)
        account.outgoing_transfer(100)
        account.express_transfer(10)
        assert account.submit_for_loan(200) == False
        
