from resource import *
from flask_restful import Api



def setup(app):
    api = Api(app)
    api.add_resource(User)