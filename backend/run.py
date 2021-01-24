from app import supa # noqa
from app.routes import * # noqa
import os

if __name__ == "__main__":
    supa.config.from_pyfile('../config.py')
    supa.run(
        host=os.environ.get("BACKEND_HOST", "127.0.0.1"),
        port=os.environ.get("BACKEND_PORT", 5000)
    )