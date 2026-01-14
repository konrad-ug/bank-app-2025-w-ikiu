from datetime import date
from src.company_account import CompanyAccount
import requests

class TestNipValidation:
    
    # sukces
    def test_create_company_valid_nip_czynny(self, mocker):
        # mock daty
        mock_date = mocker.patch("src.company_account.date")
        mock_date.today.return_value = date(2025, 1, 14)

        # mock odpowiedzi
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": {
                    "name": "Super Firma",
                    "nip": "8461627563",
                    "statusVat": "Czynny"
                },
                "requestId": "123-xyz"
            }
        }

        mock_get = mocker.patch("src.company_account.requests.get", return_value=mock_response)
        account = CompanyAccount("Firma A", "8461627563")

        assert account.nip == "8461627563"
        assert account.name == "Firma A"
        
        # weryfikacja url
        expected_url = "https://wl-test.mf.gov.pl/api/search/nip/8461627563?date=2025-01-14"
        mock_get.assert_called_with(expected_url, timeout=5)

    # porazka
    def test_create_company_not_active_vat(self, mocker):
        # mock
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Zwolniony"
                }
            }
        }
        mocker.patch("src.company_account.requests.get", return_value=mock_response)
        account = CompanyAccount("Firma B", "1234567890")

        assert account.nip == "Invalid"

    # api zwraca blad
    def test_create_company_api_error(self, mocker):
        # mock
        mock_response = mocker.Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {}
        mocker.patch("src.company_account.requests.get", return_value=mock_response)
        account = CompanyAccount("Błąd Serwera", "1234567890")

        assert account.nip == "Invalid"

    # zly format nipu
    def test_create_company_invalid_nip_len(self, mocker):
        # mock
        mock_get = mocker.patch("src.company_account.requests.get")
        account = CompanyAccount("Zły NIP", "123")

        assert account.nip == "Invalid"
        
        # upewnienie ze zapytanie nie zostalo wyslane do api
        mock_get.assert_not_called()

    # test bledu polaczenia
    def test_create_company_connection_exception(self, mocker):
        mocker.patch("src.company_account.requests.get", side_effect=requests.RequestException("Brak internetu"))
        account = CompanyAccount("Firma Offline", "1234567890")

        assert account.nip == "Invalid"