from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678900")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678900"

    # testy sprawdzajace poprawnosc peselu

    def test_pesel_too_long(self):
        account = Account("Jane", "Doe", "1234567890000")
        assert account.pesel == "Invalid"
    
    def test_pesel_too_short(self):
        account = Account("Jane", "Doe", "123")
        assert account.pesel == "Invalid"

    def test_pesel_none(self):
        account = Account("Jane", "Doe", "")
        assert account.pesel == "Invalid"

    # testy do sprawdzenia podanego kodu promocyjnego

    def test_promo_code_suffix_too_long(self):
        account = Account("Alice", "Smith", "12345678900", "PROM_XYZZ")
        assert account.balance == 0

    def test_promo_code_suffix_too_short(self):
        account = Account("Alice", "Smith", "12345678900", "PROM_XY")
        assert account.balance == 0

    def test_promo_code_prefix_wrong(self):
        account = Account("Alice", "Smith", "12345678900", "P_XYZ")
        assert account.balance == 0

    def test_promo_code_wrong(self):
        account = Account("Alice", "Smith", "12345678900", "asdhaj")
        assert account.balance == 0

    # testy do walidacji roku urodzenia przy przyznawaniu promocji

    def test_promo_code_too_old(self):
        account = Account("Alice", "Smith", "59010100000", "PROM_XYZ")
        assert account.balance == 0

    def test_promo_code_too_old_1910(self):
        account = Account("Alice", "Smith", "10100512345", "PROM_XYZ")
        assert account.balance == 0

    def test_promo_code_too_old_and_wrong_code(self):
        account = Account("Alice", "Smith", "60010112345", "djsjk")
        assert account.balance == 0

    def test_promo_code_age_ok(self):
        account = Account("Alice", "Smith", "75041512345", "PROM_XYZ")
        assert account.balance == 50

    def test_promo_code_age_ok_2010(self):
        account = Account("Alice", "Smith", "75041512345", "PROM_XYZ")
        assert account.balance == 50
    
    def test_promo_code_age_ok_wrong_code(self):
        account = Account("Alice", "Smith", "02270312345", "PROM_XY")
        assert account.balance == 0
