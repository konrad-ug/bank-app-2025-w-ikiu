# dla kont osobistych

import pytest
from src.personal_account import PersonalAccount

@pytest.fixture
def account():
    return PersonalAccount("John", "Doe", "12345678900")

@pytest.mark.parametrize("transfers, balance, loan_amount, expected_result", [
    
    # 3 wplaty z rzedu -> sukces
    ([100, 100, 100], None, 500, True),
    
    # wyplata w 3 ostatnich -> porazka
    ([100, 100, -50], 1000.0, 500, False),
    
    # za krotka historia porazka
    ([100, 100], None, 500, False),

    # warunek 1 nie ale warunek 2 tak -> sukces
    ([1000, 1000, 1000, -100, 100], 5000.0, 2000, True),

    # za mala suma -> porazka
    ([10, 10, 10, -100, -100], 500.0, 1000, False),
    
    # ujemna suma ale 3 ostatnie dodatnie -> sukces
    ([-2000, -2000, 10, 10, 10], 10000.0, 100, True),

    # suma ok ale 3 ostatnie nie -> suma
    ([1000, 1000, 1000, -100, 1000], 0.0, 1000, True),
])

def test_loan_scenarios(account, transfers, balance, loan_amount, expected_result):
    if balance is not None:
        account.balance = balance
    
    for amount in transfers:
        if amount > 0:
            account.incoming_transfer(amount)
        else:
            account.outgoing_transfer(abs(amount))

    balance_before = account.balance

    result = account.submit_for_loan(loan_amount)

    assert result == expected_result
    
    if expected_result is True:
        assert account.balance == balance_before + loan_amount
    else:
        assert account.balance == balance_before
