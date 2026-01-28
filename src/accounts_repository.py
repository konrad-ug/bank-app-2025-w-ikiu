from pymongo import MongoClient
from src.personal_account import PersonalAccount

class MongoAccountsRepository:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
        self.db = self.client.bank_db
        self.collection = self.db.accounts

    def save_all(self, registry):
        # pobranie kont z rejestru
        accounts = registry.get_all_accounts()
        
        # czyszczenie bazy
        self.collection.delete_many({})
        
        # zapis konta jako dokumenty JSON
        if accounts:
            data_to_save = [acc.to_dict() for acc in accounts]
            self.collection.insert_many(data_to_save)

    def load_all(self, registry):
        # czyszczenie rejestru aplikacji
        registry.cleanup()
        
        # dane z bazy
        accounts_data = self.collection.find()
        
        for data in accounts_data:
            # tworzenie konta na podstawie danych z bazy
            account = PersonalAccount(
                first_name=data["first_name"],
                last_name=data["last_name"],
                pesel=data["pesel"],
                balance=data.get("balance", 0.0)
            )
            # historia
            if "history" in data:
                account.transfer_history = data["history"]
            
            registry.add_account(account)