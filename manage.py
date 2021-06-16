from flask_script import Manager
from flask import Flask
from router import setup
from flask_mongoengine import MongoEngine
app = Flask(__name__)
manager = Manager(app)
setup(app)
app.config.from_mapping(
    MONGODB_SETTINGS={
        'db': 'base',
        'host': 'localhost',
        'port': 27017,
        'connect': True,
        'username': 'jonney',
        'password': '123456',
        # 'authentication_source': 'admin'
    }
)
db = MongoEngine(app)


if __name__ == '__main__':
    app.run()