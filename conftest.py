import pytest
import threading
import time
from app.api import app

@pytest.fixture(scope="session", autouse=True)
def start_flask():
    server = threading.Thread(
        target=app.run,
        kwargs={
            "host": "127.0.0.1",
            "port": 5000,
            "debug": False,
            "use_reloader": False
        }
    )
    server.daemon = True
    server.start()

    time.sleep(1)
    yield
