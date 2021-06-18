from resource import *
from flask_restful import Api


def setup(app):
    api = Api(app)
    api.add_resource(UserResource, '/user')
    api.add_resource(ProxyResource, '/proxy')
    api.add_resource(AddressResource, '/address')
    api.add_resource(EmailResource, '/email')
    api.add_resource(AccountResource, '/account')
