from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "12345678900")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678900"

    # testy sprawdzajace poprawnosc peselu

    def test_pesel_too_long(self):
        account = PersonalAccount("Jane", "Doe", "1234567890000")
        assert account.pesel == "Invalid"
    
    def test_pesel_too_short(self):
        account = PersonalAccount("Jane", "Doe", "123")
        assert account.pesel == "Invalid"

    def test_pesel_none(self):
        account = PersonalAccount("Jane", "Doe", "")
        assert account.pesel == "Invalid"

    # testy do sprawdzenia podanego kodu promocyjnego

    def test_promo_code_suffix_too_long(self):
        account = PersonalAccount("Alice", "Smith", "12345678900", "PROM_XYZZ")
        assert account.balance == 0

    def test_promo_code_suffix_too_short(self):
        account = PersonalAccount("Alice", "Smith", "12345678900", "PROM_XY")
        assert account.balance == 0

    def test_promo_code_prefix_wrong(self):
        account = PersonalAccount("Alice", "Smith", "12345678900", "P_XYZ")
        assert account.balance == 0

    def test_promo_code_wrong(self):
        account = PersonalAccount("Alice", "Smith", "12345678900", "asdhaj")
        assert account.balance == 0

    # testy do walidacji roku urodzenia przy przyznawaniu promocji

    def test_promo_code_too_old(self):
        account = PersonalAccount("Alice", "Smith", "59010100000", "PROM_XYZ")
        assert account.balance == 0

    def test_promo_code_too_old_1910(self):
        account = PersonalAccount("Alice", "Smith", "10100512345", "PROM_XYZ")
        assert account.balance == 0

    def test_promo_code_too_old_and_wrong_code(self):
        account = PersonalAccount("Alice", "Smith", "60010112345", "djsjk")
        assert account.balance == 0

    def test_promo_code_age_ok(self):
        account = PersonalAccount("Alice", "Smith", "75041512345", "PROM_XYZ")
        assert account.balance == 50

    def test_promo_code_age_ok_2010(self):
        account = PersonalAccount("Alice", "Smith", "75041512345", "PROM_XYZ")
        assert account.balance == 50
    
    def test_promo_code_age_ok_wrong_code(self):
        account = PersonalAccount("Alice", "Smith", "02270312345", "PROM_XY")
        assert account.balance == 0.0

    # testy dla company account

    def test_company_account_nip_ok(self):
        account = CompanyAccount("Firma", "1234567890")
        assert account.nip == "1234567890"

    def test_company_account_nip_wrong(self):
        account = CompanyAccount("Firma", "123")
        assert account.nip == "Invalid"