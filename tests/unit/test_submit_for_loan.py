from src.personal_account import PersonalAccount

def test_loan_success_3_transfers():
    account = PersonalAccount("John", "Doe", "12345678900")
    
    account.incoming_transfer(100)
    account.incoming_transfer(100)
    account.incoming_transfer(100)

    account.balance = 10.0 
    result = account.submit_for_loan(500)
    
    assert result is True
    assert account.balance == 510.0 

def test_loan_fail_last_negative_in_history():
    account = PersonalAccount("John", "Doe", "12345678900")
    
    account.balance = 1000.0
    
    account.incoming_transfer(100)
    account.incoming_transfer(100)
    account.outgoing_transfer(100)
    
    result = account.submit_for_loan(500)
    
    assert result is False
    assert account.balance == 1100.0

def test_loan_fail_no_history():
    account = PersonalAccount("John", "Doe", "12345678900")
    account.balance = 1000000.0
    account.incoming_transfer(500)
    
    result = account.submit_for_loan(500)
    assert result is False


def test_loan_success_1_f_2_s():
    account = PersonalAccount("John", "Doe", "12345678900")
    
    account.balance = 5000.0
    
    account.incoming_transfer(600)
    account.incoming_transfer(600)
    account.incoming_transfer(600)
    account.outgoing_transfer(100)
    account.incoming_transfer(200)
    
    account.balance = 100.0 
    
    result = account.submit_for_loan(1500)
    
    assert result is True
    assert account.balance == 100.0 + 1500

def test_loan_fail_f_2():
    account = PersonalAccount("John", "Doe", "12345678900")
    account.balance = 500.0
    
    account.incoming_transfer(10)
    account.incoming_transfer(10)
    account.incoming_transfer(10)
    account.outgoing_transfer(100)
    account.outgoing_transfer(100)
    
    result = account.submit_for_loan(1000)
    assert result is False

def test_loan_fail_1_f_2_f():
    account = PersonalAccount("John", "Doe", "12345678900")
    account.balance = 200.0
    
    account.incoming_transfer(100)
    account.incoming_transfer(100)
    account.express_transfer(50)
    
    result = account.submit_for_loan(500)
    assert result is False

def test_loan_success_1_s_2_f():
    account = PersonalAccount("John", "Doe", "12345678900")
    account.balance = 10000.0
    
    account.outgoing_transfer(2000) 
    account.outgoing_transfer(2000)

    account.incoming_transfer(10)
    account.incoming_transfer(10)
    account.incoming_transfer(10)
    
    account.balance = 0.0
    result = account.submit_for_loan(100)
    
    assert result is True
    assert account.balance == 100.0



        
