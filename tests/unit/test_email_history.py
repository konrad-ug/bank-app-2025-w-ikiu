import pytest
from datetime import date
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestEmailHistory:
    
    @pytest.fixture
    def mock_smtp(self, mocker):
        return mocker.Mock()

    @pytest.fixture
    def personal_account(self):
        acc = PersonalAccount("Jan", "Kowalski", "12345678901")
        acc.incoming_transfer(100)
        acc.express_transfer(1)
        acc.incoming_transfer(500)
        acc.transfer_history = [100, -1, 500] 
        return acc

    @pytest.fixture
    def company_account(self, mocker):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"result": {"subject": {"statusVat": "Czynny"}}}
        mocker.patch("src.company_account.requests.get", return_value=mock_resp)
        
        acc = CompanyAccount("Firma", "1234567890")
        acc.transfer_history = [5000, -1000, 500]
        return acc

    # testy konta personalnego

    # sukces
    def test_send_history_personal_success(self, personal_account, mock_smtp, mocker):
        mock_date = mocker.patch("src.personal_account.date")
        mock_date.today.return_value = date(2025, 12, 10)

        mock_smtp.send.return_value = True
        result = personal_account.send_history_via_email("jan@test.pl", mock_smtp)

        assert result is True
        
        mock_smtp.send.assert_called_once()
        args = mock_smtp.send.call_args[0]
        
        assert args[0] == "Account Transfer History 2025-12-10"
        assert args[1] == "Personal account history: [100, -1, 500]"
        assert args[2] == "jan@test.pl"

    # porazka
    def test_send_history_personal_failure(self, personal_account, mock_smtp, mocker):
        mock_date = mocker.patch("src.personal_account.date")
        mock_date.today.return_value = date(2025, 12, 10)
        
        mock_smtp.send.return_value = False
        result = personal_account.send_history_via_email("jan@test.pl", mock_smtp)

        assert result is False
        mock_smtp.send.assert_called_once()


    # TESTY DLA KONTA FIRMOWEGO

    # sukces
    def test_send_history_company_success(self, company_account, mock_smtp, mocker):
        mock_date = mocker.patch("src.company_account.date")
        mock_date.today.return_value = date(2025, 12, 10)

        mock_smtp.send.return_value = True
        result = company_account.send_history_via_email("szef@firma.pl", mock_smtp)

        assert result is True
        
        args = mock_smtp.send.call_args[0]
        assert args[0] == "Account Transfer History 2025-12-10"
        assert args[1] == "Company account history: [5000, -1000, 500]"
        assert args[2] == "szef@firma.pl"