# dla kont firmowych

import pytest
from src.company_account import CompanyAccount
# w company account do fixture jest name i nip, bede tez brac wartosc kredytu i historie wplat ale to do parametrize

@pytest.fixture
def account():
    return CompanyAccount("Firma ABC", "1234567890")

# @pytest.mark.parametrize( "argumenty, w, takiej, formie", [
#     (wartosci, w, takiej, formie),
#     (nastepny, test)
# ])

@pytest.mark.parametrize("transfers, balance, loan_amount, expected_result", [

    # oba warunki spelnione
    ([1000, 90, -100, 3000, -1775, 8000], 1000+90-100+3000-1775+8000+50, 50, True),

    # zaden z warunkow nie jest spelniony
    ([100, -5, 20], 100-5+20, 1000, False),

    # tylko warunek z zusem
    ([1000, 90, -100, 1000, -1775, -20], 1000+90-100+1000-1775-20, 1000, False),

    # tylko warunek z 2x wiekszym saldem
    ([1000, 90, -100, 1000, -20], 1000+90-100+1000-20, 50, False)

])

def test_loan_scenarios_company(account, transfers, balance, loan_amount, expected_result):
    if balance is not None:
        account.balance = balance

    for amount in transfers:
        if amount > 0:
            account.incoming_transfer(amount)
        else:
            account.outgoing_transfer(abs(amount))

    balance_before = account.balance

    result = account.take_loan(loan_amount)
    assert result == expected_result

    if expected_result is True:
        assert account.balance == balance_before + loan_amount
    else:
        assert account.balance == balance_before
