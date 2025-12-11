import requests

class TestTransfers:
    url = "http://127.0.0.1:5000"
    
    account_data = {
        "name": "james",
        "surname": "hetfield",
        "pesel": "89092909825"
    }

    def setup_method(self):
        response = requests.get(f"{self.url}/api/accounts")
        if response.status_code == 200:
            for account in response.json():
                requests.delete(f"{self.url}/api/accounts/{account['pesel']}")
        
        requests.post(f"{self.url}/api/accounts", json=self.account_data)

    def test_incoming_transfer(self):
        transfer_data = {
            "amount": 500,
            "type": "incoming"
        }
        pesel = self.account_data['pesel']
        
        response = requests.post(f"{self.url}/api/accounts/{pesel}/transfer", json=transfer_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Transfer successful"
        
        response = requests.get(f"{self.url}/api/accounts/{pesel}")
        assert response.status_code == 200
        assert response.json()["balance"] == 500

    def test_outgoing_transfer_insufficient_funds(self):
        transfer_data = {
            "amount": 1200,
            "type": "outgoing"
        }
        pesel = self.account_data['pesel']
        
        # proba wyplaty 1200 z konta na 0
        response = requests.post(f"{self.url}/api/accounts/{pesel}/transfer", json=transfer_data)
        
        assert response.status_code == 422
        data = response.json()
        assert data["message"] == "There was an issue with transfer"

    # test do ekspresowego przelewu
    def test_express_transfer(self):
        pesel = self.account_data['pesel']
        requests.post(f"{self.url}/api/accounts/{pesel}/transfer", json={"amount": 1000, "type": "incoming"})

        transfer_data = {
            "amount": 500,
            "type": "express"
        }
        
        response = requests.post(f"{self.url}/api/accounts/{pesel}/transfer", json=transfer_data)
        assert response.status_code == 200
        
        response = requests.get(f"{self.url}/api/accounts/{pesel}")
        assert response.json()["balance"] == 499

    # proba utworzenia konta z tym samym peselem
    def test_create_duplicate_account(self):
        response = requests.post(f"{self.url}/api/accounts", json=self.account_data)
        
        assert response.status_code == 409
        assert response.json()["message"] == "Account with this pesel already exists"