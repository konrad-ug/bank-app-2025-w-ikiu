import pytest
from src.accounts_repository import MongoAccountsRepository
from src.personal_account import PersonalAccount
from src.registry import AccountsRegistry

class TestMongoRepository:
    
    # zapis do bazy
    def test_save_all_clears_db_and_saves_accounts(self, mocker):
        # mock mongoclient
        mock_client = mocker.patch("src.accounts_repository.MongoClient")
        mock_collection = mock_client.return_value.bank_db.accounts
        
        registry = AccountsRegistry()
        acc = PersonalAccount("Jan", "Testowy", "12345678901", balance=100.0)
        registry.add_account(acc)
        
        repo = MongoAccountsRepository()
        
        repo.save_all(registry)
        mock_collection.delete_many.assert_called_once_with({})
        
        assert mock_collection.insert_many.called
        args = mock_collection.insert_many.call_args[0][0]
        assert args[0]["first_name"] == "Jan"
        assert args[0]["balance"] == 100.0

    # test odczytu
    def test_load_all_clears_registry_and_loads_from_db(self, mocker):
        # mock mongoclient
        mock_client = mocker.patch("src.accounts_repository.MongoClient")
        mock_collection = mock_client.return_value.bank_db.accounts
        
        fake_db_data = [{
            "first_name": "Anna",
            "last_name": "Kowalska",
            "pesel": "99999999999",
            "balance": 500.0,
            "history": [-100, 200]
        }]
        mock_collection.find.return_value = fake_db_data
        
        repo = MongoAccountsRepository()
        registry = AccountsRegistry()
        registry.add_account(PersonalAccount("Do", "Usuniecia", "00000000000"))
        
        repo.load_all(registry)
        
        assert registry.number_of_accounts() == 1
        loaded_acc = registry.get_account_by_pesel("99999999999")
        assert loaded_acc is not None
        assert loaded_acc.first_name == "Anna"
        assert loaded_acc.balance == 500.0
        assert loaded_acc.transfer_history == [-100, 200]