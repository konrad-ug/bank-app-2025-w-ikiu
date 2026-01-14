from src.account import Account
import os
import requests
from datetime import date

class CompanyAccount(Account):
    def __init__(self, name, nip):
        super().__init__(name, "")
        self.name = name

        # walidacja nipu
        if not (isinstance(nip, str) and len(nip) == 10 and nip.isdigit()):
            self.nip = "Invalid"
            return

        # walidacja do feature 18
        if not self._check_nip_in_mf(nip):
            self.nip = "Invalid"
            return

        self.nip = nip

    MF_DEFAULT_URL = "https://wl-test.mf.gov.pl"

    # do feature 18
    def _check_nip_in_mf(self, nip):
        base_url = os.getenv("BANK_APP_MF_URL", self.MF_DEFAULT_URL)
        today = date.today().isoformat()

        url = f"{base_url}/api/search/nip/{nip}?date={today}"
        
        try:
            response = requests.get(url, timeout=5)

            if response.status_code != 200:
                return False

            data = response.json()
            subject = data.get("result", {}).get("subject")

            if not subject:
                return False

            return subject.get("statusVat") == "Czynny"
            
        except requests.RequestException:
            return False
        
    # feature 19 - wysylanie historii emailem
    def send_history_via_email(self, to_email, smtp_client):
        today = date.today()
        subject = f"Account Transfer History {today}"
        
        body = f"Company account history: {self.transfer_history}"
        
        return smtp_client.send(subject, body, to_email)

    def express_transfer(self, amount):
        express_transfer_fee = 5.0
        total = amount + express_transfer_fee
        if amount > 0 and self.balance and (self.balance - total) >= express_transfer_fee*(-1):
            self.balance -= (amount + express_transfer_fee)
            self.transfer_history.append(amount*(-1))
            self.transfer_history.append(express_transfer_fee*(-1))
            return True
        return False
    
    def take_loan(self, amount):
        if self._is_twice_as_big(amount) and self._zus_transfer_exists():
            self.balance += amount
            return True
        return False

    def _is_twice_as_big(self, amount):
        if amount*2 <= self.balance:
            return True
        return False
    
    def _zus_transfer_exists(self):
        if -1775 in self.transfer_history:
            return True
        else:
            return False