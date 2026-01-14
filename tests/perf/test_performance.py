import pytest
import time
from app.api import app, registry

class TestPerformance:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = app.test_client()
        registry.cleanup()

    # tworzenie i usuwanie konta 100 razy
    def test_perf_create_and_delete_account(self):
        for i in range(100):
            pesel = f"90010100{i:03d}"
            payload = {
                "first_name": "Perf",
                "last_name": "Test",
                "pesel": pesel
            }

            start_time = time.time()
            
            res_create = self.client.post("/api/accounts", json=payload)
            assert res_create.status_code == 201, f"Failed to create account in iter {i}"

            res_delete = self.client.delete(f"/api/accounts/{pesel}")
            assert res_delete.status_code == 200, f"Failed to delete account in iter {i}"

            end_time = time.time()
            duration = end_time - start_time

            assert duration < 0.5, f"Iteration {i} took too long: {duration}s"

    # 100 przelewow przychodzacych
    def test_perf_incoming_transfers(self):
        pesel = "12345678901"
        self.client.post("/api/accounts", json={
            "first_name": "Jan",
            "last_name": "Kowalski",
            "pesel": pesel
        })

        transfer_amount = 100
        repetitions = 100

        for i in range(repetitions):
            payload = {"amount": transfer_amount}
            
            start_time = time.time()
            
            res = self.client.post(f"/api/accounts/{pesel}/transfer", json=payload)
            
            end_time = time.time()
            duration = end_time - start_time

            assert res.status_code == 200, f"Transfer failed in iter {i}"
            assert duration < 0.5, f"Transfer {i} took too long: {duration}s"

        # saldo
        res_get = self.client.get(f"/api/accounts/{pesel}")
        assert res_get.status_code == 200
        
        data = res_get.get_json()
        expected_balance = transfer_amount * repetitions
        
        assert data["balance"] == expected_balance, f"Balance mismatch! Expected {expected_balance}, got {data['balance']}"