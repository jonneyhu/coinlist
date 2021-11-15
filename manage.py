# from flask_script import Manager
from flask_cors import CORS

from application import app
from router import setup
from flask_mongoengine import MongoEngine

# manager = Manager(app)
setup(app)
CORS(app)
db = MongoEngine(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)