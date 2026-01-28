from flask import Flask, request, jsonify
from src.personal_account import PersonalAccount
from src.registry import AccountsRegistry
from src.accounts_repository import MongoAccountsRepository

app = Flask(__name__)
registry = AccountsRegistry()
repository = MongoAccountsRepository()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Request: create account {data}")
    
    # obsluga i firstname i po prostu name
    first_name = data.get("first_name") or data.get("name")
    last_name = data.get("last_name") or data.get("surname")
    pesel = data.get("pesel")

    if not (first_name and last_name and pesel):
        return jsonify({"message": "Missing required data"}), 400

    account = PersonalAccount(first_name, last_name, pesel)
    
    # feature 16
    success = registry.add_account(account)

    if success:
        return jsonify({"message": "Account created"}), 201
    else:
        return jsonify({"message": "Account with this pesel already exists"}), 409


@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    accounts = registry.get_all_accounts()
    return jsonify([
        {"first_name": acc.first_name, "last_name": acc.last_name, "pesel": acc.pesel, "balance": acc.balance}
        for acc in accounts
    ]), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    count = registry.number_of_accounts()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.get_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    return jsonify({
        "first_name": account.first_name,
        "last_name": account.last_name,
        "pesel": account.pesel,
        "balance": account.balance
    }), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    account = registry.get_account_by_pesel(pesel)
    
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    if "first_name" in data:
        account.first_name = data["first_name"]
    elif "name" in data:
        account.first_name = data["name"]

    if "last_name" in data:
        account.last_name = data["last_name"]
    elif "surname" in data:
        account.last_name = data["surname"]
    
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    is_deleted = registry.delete_account(pesel)

    if is_deleted:
        return jsonify({"message": "Account deleted"}), 200
    else:
        return jsonify({"message": "Account not found"}), 404

# feature 17
@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer(pesel):
    data = request.get_json()
    
    if not data or "amount" not in data:
        return jsonify({"message": "Invalid request body"}), 400

    account = registry.get_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    amount = data["amount"]
    transfer_type = data.get("type", "incoming")

    success = False
    if transfer_type == "incoming":
        account.incoming_transfer(amount)
        success = True 
    elif transfer_type == "outgoing":
        success = account.outgoing_transfer(amount)
        if success is None: success = True
    elif transfer_type == "express":
        success = account.express_transfer(amount)
    else:
        return jsonify({"message": "Invalid transfer type"}), 400

    if success:
        return jsonify({"message": "Transfer successful", "balance": account.balance}), 200
    else:
        return jsonify({"message": "There was an issue with transfer"}), 422
    
@app.route("/api/accounts/save", methods=['POST'])
def save_registry():
    try:
        repository.save_all(registry)
        return jsonify({"message": "Registry saved to database"}), 200
    except Exception as e:
        # Ten błąd wystąpi u Ciebie lokalnie (brak Dockera), ale na GitHubie przejdzie
        return jsonify({"message": f"Database error: {str(e)}"}), 500

@app.route("/api/accounts/load", methods=['POST'])
def load_registry():
    try:
        repository.load_all(registry)
        return jsonify({"message": "Registry loaded from database"}), 200
    except Exception as e:
        return jsonify({"message": f"Database error: {str(e)}"}), 500
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)