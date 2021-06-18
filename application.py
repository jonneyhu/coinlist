
from flask import Flask
app = Flask(__name__)
app.config.from_mapping(
    MONGODB_SETTINGS={
        'db': 'base',
        'host': 'localhost',
        'port': 27017,
        'connect': True,
        'username': 'root',
        'password': '',
        # 'authentication_source': 'admin'
    }
)
app.config.from_pyfile('config.py')