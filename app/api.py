from flask import Flask, request, jsonify
from src.personal_account import PersonalAccount
from src.registry import AccountsRegistry

app = Flask(__name__)
registry = AccountsRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Request: create account {data}")
    
    account = PersonalAccount(data["name"], data["surname"], data["pesel"])
    
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
        {"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance}
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
        "name": account.first_name,
        "surname": account.last_name,
        "pesel": account.pesel,
        "balance": account.balance
    }), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    account = registry.get_account_by_pesel(pesel)
    
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
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
    
    if not data or "amount" not in data or "type" not in data:
        return jsonify({"message": "Invalid request body"}), 400

    account = registry.get_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    amount = data["amount"]
    transfer_type = data["type"]

    success = False
    if transfer_type == "incoming":
        success = account.incoming_transfer(amount)
    elif transfer_type == "outgoing":
        success = account.outgoing_transfer(amount)
    elif transfer_type == "express":
        success = account.express_transfer(amount)
    else:
        return jsonify({"message": "Invalid transfer type"}), 400

    if success:
        return jsonify({"message": "Transfer successful"}), 200
    else:
        return jsonify({"message": "There was an issue with transfer"}), 422
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)