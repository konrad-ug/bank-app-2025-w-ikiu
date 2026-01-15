import pytest
from src.registry import AccountsRegistry
from src.personal_account import PersonalAccount

@pytest.fixture
def registry():
    return AccountsRegistry()


# do testow licznika kont
@pytest.mark.parametrize("accounts_to_add, expected_count", [
    ([], 0), # 0 kont
    ([("Jan", "Kowalski", "12345678900")], 1), # jedno konto
    ([("Jan", "K", "12345678900"), ("Anna", "N", "98765432100")], 2) # dwa konta
])

def test_registry_add_and_count(registry, accounts_to_add, expected_count):
    for first_name, last_name, pesel in accounts_to_add:
        acc = PersonalAccount(first_name, last_name, pesel)
        registry.add_account(acc)
    
    assert registry.number_of_accounts() == expected_count
    assert len(registry.get_all_accounts()) == expected_count


# do testow wyszukiwania po peselu
@pytest.mark.parametrize("pesel_to_find, should_find", [
    ("12345678900", True),  # istnieje
    ("99999999999", False), # nie istnieje
    ("", False)
])

def test_registry_search_by_pesel(registry, pesel_to_find, should_find):
    known_pesel = "12345678900"
    account = PersonalAccount("Test", "User", known_pesel)
    registry.add_account(account)

    found_account = registry.get_account_by_pesel(pesel_to_find)

    if should_find:
        assert found_account is not None
        assert found_account.pesel == pesel_to_find
    else:
        assert found_account is None

def test_add_duplicate_account_returns_false(registry):
    pesel = "12345678900"
    acc1 = PersonalAccount("Jan", "Pierwszy", pesel)
    assert registry.add_account(acc1) is True

    acc2 = PersonalAccount("Anna", "Druga", pesel)
    result = registry.add_account(acc2)

    assert result is False

    assert registry.number_of_accounts() == 1