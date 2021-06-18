import datetime

from flask import g
from flask_restful import Resource, reqparse, fields, marshal_with
import pymongo
from model.resource import Proxy
from resource import auth
from util.page import Page

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.base

email_parser = reqparse.RequestParser()
email_parser.add_argument('email', type=str)
email_parser.add_argument('password', type=str)
email_parser.add_argument('assist', type=str)

address_parser = reqparse.RequestParser()
address_parser.add_argument('address', type=str, required=True)
address_parser.add_argument('postcode', type=str, required=True)
address_parser.add_argument('country', type=str, required=True)

proxy_parser = reqparse.RequestParser()
proxy_parser.add_argument('server', type=str, required=True)
proxy_parser.add_argument('origin_ip', type=str, required=True)
proxy_parser.add_argument('country', type=str, required=True)

proxy_get_parser = reqparse.RequestParser()
proxy_get_parser.add_argument('page', type=int, required=True)
proxy_get_parser.add_argument('limit', type=int, default=10)

account_parser = reqparse.RequestParser()
account_parser.add_argument('amount', type=int, default=10)
account_parser.add_argument('country', type=str)

make_parser = reqparse.RequestParser()
make_parser.add_argument('country', type=str)
make_parser.add_argument('email', type=str)
make_parser.add_argument('auth_info', type=str)
make_parser.add_argument('secret', type=str)


class EmailResource(Resource):
    def get(self):
        args = proxy_get_parser.parse_args()
        results = db.email.find()
        page = Page(results, args['page'], args['limit'])
        return {'code': 200, 'msg': 'success', 'data': page.page()}

    def post(self):
        args = email_parser.parse_args()
        email = {
            'email': args['email'],
            'password': args['password'],
            'assist': args['assist'],
            'is_used': False,
        }
        db.email.insert([email])
        return {'code': 200, 'msg': 'success'}


class AddressResource(Resource):
    def get(self):
        args = proxy_get_parser.parse_args()
        results = db.address.find()
        page = Page(results, args['page'], args['limit'])
        return {'code': 200, 'msg': 'success', 'data': page.page()}

    def post(self):
        args = address_parser.parse_args()
        address = {
            'address': args['address'],
            'postcode': args['postcode'],
            'country': args['country']
        }
        db.address.insert([address])
        return {'code': 200, 'msg': 'success'}


class ProxyResource(Resource):
    def get(self):
        args = proxy_get_parser.parse_args()
        results = db.proxy.find()
        page = Page(results, args['page'], args['limit'])
        return {'code': 200, 'msg': 'success', 'data': page.page()}

    def post(self):
        args = proxy_parser.parse_args()
        proxy = Proxy(server=args['server'], origin_ip=args['origin_ip'], country=args['country'])
        proxy.save()
        return {'code': 200, 'msg': 'success'}


class AccountResource(Resource):
    def get(self):
        results = db.account.find({'operate_status': 1})
        args = proxy_get_parser.parse_args()
        page = Page(results, args['page'], args['limit'])
        return {'code': 200, 'msg': 'success', 'data': page.page()}

    @auth.login_required
    def post(self):
        amount = account_parser.parse_args()['amount']
        country = account_parser.parse_args()['country']
        # 计算最小资源
        email_count = db.email.find({'is_used': False, 'country': country}).count()
        address_count = db.address.find({'is_used': False, 'country': country}).count()
        proxies = db.proxy.find({'country': country, 'times': {'$lt': 5}})
        proxy_count = 0
        for p in proxies:
            proxy_count += 5 - p.times
        s_count = sorted([email_count, address_count, proxy_count])
        if s_count[0] < amount:
            return {'code': 400, 'msg': '资源不足'}
        email = db.email.find({'is_used': False, 'country': country}).limit(amount)
        address = db.address.find({'is_used': False, 'country': country}).limit(amount)
        email = [i for i in email]
        address = [i for i in address]
        proxies = [i for i in proxies]
        for i in range(5):
            account = {
                'email': email[i]['_id'],
                'address': address[i]['_id'],
                'proxy': proxies[i]['_id'],
                'cl_password': '123456',
                'cl_username': '',
                'user': '',
                'register_status': 0,
                'secret': '',
                'operator': g.user,
                'operate_status': 0,
                'auth_info': '',
                'remark': '',
                'submit_at': '',
                'distribution_at': datetime.datetime.now(),
                'check_at': ''
            }
            db.account.insert_one(account)
        return {'code': 200, 'msg': 'success'}


class AvailableResource(Resource):
    def get(self):
        country = make_parser.parse_args()['country']
        # 计算最小资源
        email_count = db.email.find({'is_used': False, 'country': country}).count()
        address_count = db.address.find({'is_used': False, 'country': country}).count()
        proxies = db.proxy.find({'country': country, 'times': {'$lt': 5}})
        proxy_count = 0
        for p in proxies:
            proxy_count += 5 - p.times
        s_count = sorted([email_count, address_count, proxy_count])
        return {'code': 200, 'data': s_count}


class MakeAccount(Resource):
    def get(self):
        results = db.account.aggregate([{'$math':{'operate_status': 1}},
                                        {'$lookup':{'from':'email','localField':'email','foreignField':'_id','as':'email_info'}},
                                        {'$lookup':{'from':'address','localField':'address','foreignField':'_id','as':'address_info'}},
                                        {'$lookup':{'from':'proxy','localField':'proxy','foreignField':'_id','as':'proxy_info'}},
                                        {'$project':{'email':0,'address':0,'proxy':0}}
                                        ])
        args = proxy_get_parser.parse_args()
        page = Page(results, args['page'], args['limit'])
        return {'code': 200, 'msg': 'success', 'data': page.page()}

    def post(self):
        args = make_parser.parse_args()
        email = db.email.find_one({'email': args['email']})
        db.account.update({'email': email['_id']},
                          {'$set': {'auth_info': args['auth_info'], 'secret': args['secret']}, 'operate_status': 1})
        return {'code':200,'msg':'success'}
