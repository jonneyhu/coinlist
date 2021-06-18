# from flask_script import Manager
from application import app
from router import setup
from flask_mongoengine import MongoEngine

# manager = Manager(app)
setup(app)

db = MongoEngine(app)


if __name__ == '__main__':
    app.run()