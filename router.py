# from resource import *
# from flask_restful import Api


# def setup(app):
#     api = Api(app)
#     api.add_resource(UserResource, '/user')
#     api.add_resource(Login, '/user/login')
#     api.add_resource(ProxyResource, '/proxy')
#     api.add_resource(AddressResource, '/address')
#     api.add_resource(EmailResource, '/email')
#     api.add_resource(AccountResource, '/account')
#     api.add_resource(AvailableResource, '/available')
#     api.add_resource(MakeAccount, '/account/make')
#     api.add_resource(FinishedAccount, '/account/finished')
#     api.add_resource(SelfAccount, '/account/self')
#     api.add_resource(SyncAccount, '/account/sync')
import time

if __name__ == '__main__':
    # a = [1,23,4]
    # b= [1,2,4,56,6]
    # time.sleep(20)
    # print(set(b).difference(set(a)))
    a = [(1,2),(2,3)]
    if (1,2) not in a:
        print(a)