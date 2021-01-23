from app import supa
from app.routes import *

if __name__ == "__main__":
    supa.config.from_pyfile('../config.py')
    supa.run(host='127.0.0.1', port=5000, debug=True)