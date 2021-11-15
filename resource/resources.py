import datetime
import json

from flask import g
from flask_restful import Resource, reqparse, fields, marshal_with
import pymongo
from model.resource import Proxy
from .user import auth
from util.page import Page

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
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
proxy_get_parser.add_argument('email', type=str)
proxy_get_parser.add_argument('register_status', type=str)
proxy_get_parser.add_argument('use_status', type=str)
proxy_get_parser.add_argument('country', type=str)

account_parser = reqparse.RequestParser()
account_parser.add_argument('amount', type=int, default=10)
account_parser.add_argument('country', type=str)

make_parser = reqparse.RequestParser()
make_parser.add_argument('country', type=str)
make_parser.add_argument('email', type=str)
make_parser.add_argument('auth_info', type=str)
make_parser.add_argument('secret', type=str)

sync_parser = reqparse.RequestParser()
sync_parser.add_argument('email', type=str)

distribute_parser = reqparse.RequestParser()
distribute_parser.add_argument('username', type=str)
distribute_parser.add_argument('accounts')

conditions_parser = reqparse.RequestParser()
conditions_parser.add_argument('email')
conditions_parser.add_argument('check_status')
conditions_parser.add_argument('country')
conditions_parser.add_argument('email')

self_parser = reqparse.RequestParser()
self_parser.add_argument('can_use', type=int)
self_parser.add_argument('email', type=str)


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
            'country': args['country'],
            'is_used': False
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
    # 获取所有提交的账户
    def get(self):
        args = proxy_get_parser.parse_args()
        conditions = {'operate_status': 1}
        if args['country']:
            conditions['country'] = args['country']
        if args['use_status']:
            if args['use_status'] == '0':
                conditions['user'] = ''
            else:
                conditions['user'] = {'$ne': ''}
        if args['register_status']:
            conditions['register_status'] = int(args['register_status'])

        def cursor(limit, skip):
            result = db.account.aggregate([{'$match': conditions},
                                           {'$lookup': {'from': 'email', 'localField': 'email', 'foreignField': '_id',
                                                        'as': 'email_info'}},
                                           {'$lookup': {'from': 'address', 'localField': 'address',
                                                        'foreignField': '_id',
                                                        'as': 'address_info'}},
                                           {'$lookup': {'from': 'proxy', 'localField': 'proxy', 'foreignField': '_id',
                                                        'as': 'proxy_info'}},
                                           {'$project': {'email': 0, 'address': 0, 'proxy': 0}},
                                           {'$limit': limit},
                                           {'$skip': skip}
                                           ])
            count = db.account.find({'operate_status': 1}).count()
            return result, count

        page = Page(cursor, args['page'], args['limit'])
        return {'code': 200, 'msg': 'success', 'data': page.page()}

    # 分配账户
    @auth.login_required
    def post(self):
        args = distribute_parser.parse_args()
        username = args['username']
        accounts = json.loads(args['accounts'])
        emails = db.email.find({'email': {'$in': accounts}})
        db.account.update({'email': {'$in': [i['_id'] for i in emails]}}, {'$set': {'user': username}})
        return {'code': 200, 'msg': 'success'}


class AvailableResource(Resource):
    def get(self):
        country = make_parser.parse_args()['country']
        # 计算最小资源
        email_count = db.email.find({'is_used': False}).count()
        address_count = db.address.find({'is_used': False, 'country': country}).count()
        proxies = db.proxy.find({'country': country, 'times': {'$lt': 5}})
        proxy_count = 0
        for p in proxies:
            proxy_count += 5 - p['times']
        s_count = sorted([email_count, address_count, proxy_count])
        return {'code': 200, 'data': s_count[0]}


class MakeAccount(Resource):
    # 获取制作中的账户
    @auth.login_required
    def get(self):
        def cursor(limit, skip):
            result = db.account.aggregate([{'$match': {'operate_status': 0, 'operator': g.user.username}},
                                           {'$lookup': {'from': 'email', 'localField': 'email', 'foreignField': '_id',
                                                        'as': 'email_info'}},
                                           {'$lookup': {'from': 'address', 'localField': 'address',
                                                        'foreignField': '_id',
                                                        'as': 'address_info'}},
                                           {'$lookup': {'from': 'proxy', 'localField': 'proxy', 'foreignField': '_id',
                                                        'as': 'proxy_info'}},
                                           {'$project': {'email': 0, 'address': 0, 'proxy': 0}},
                                           {'$limit': limit},
                                           {'$skip': skip}
                                           ])
            count = db.account.find({'operate_status': 0, 'operator': g.user.username}).count()
            return result, count

        args = proxy_get_parser.parse_args()
        page = Page(cursor, args['page'], args['limit'])
        return {'code': 200, 'msg': 'success', 'data': page.page()}

    # 批量创建账户
    @auth.login_required
    def post(self):
        amount = account_parser.parse_args()['amount']
        country = account_parser.parse_args()['country']
        # 计算最小资源
        email_count = db.email.find({'is_used': False}).count()
        address_count = db.address.find({'is_used': False, 'country': country}).count()
        proxies = db.proxy.find({'country': country, 'times': {'$lt': 5}})
        proxies = [i for i in proxies]
        proxy_count = 0
        for p in proxies:
            proxy_count += 5 - p['times']
        s_count = sorted([email_count, address_count, proxy_count])
        if s_count[0] < amount:
            return {'code': 400, 'msg': '资源不足'}
        email = db.email.find({'is_used': False}).limit(amount)
        address = db.address.find({'is_used': False, 'country': country}).limit(amount)
        email = [i for i in email]
        address = [i for i in address]

        with client.start_session(causal_consistency=True) as session:
            with session.start_transaction():
                for i in range(amount):
                    email[i]['is_used'] = True
                    db.email.find_one_and_update({'_id': email[i]['_id']}, {'$set': email[i]})
                    address[i]['is_used'] = True
                    db.address.find_one_and_update({'_id': address[i]['_id']}, {'$set': address[i]})
                    proxies[i]['times'] = proxies[i]['times'] + 1
                    db.proxy.find_one_and_update({'_id': proxies[i]['_id']}, {'$set': proxies[i]})
                    account = {
                        'email': email[i]['_id'],
                        'address': address[i]['_id'],
                        'proxy': proxies[i]['_id'],
                        'cl_password': '123456',
                        'cl_username': '',
                        'country': country,
                        'user': '',
                        'can_use': 0,
                        'register_status': 0,
                        'secret': '',
                        'operator': g.user.username,
                        'operate_status': 0,
                        'auth_info': '',
                        'remark': '',
                        'submit_at': '',
                        'distribution_at': datetime.datetime.now(),
                        'check_at': ''
                    }
                    db.account.insert_one(account)

                return {'code': 200, 'msg': 'success'}

    # 提交账户
    @auth.login_required
    def put(self):
        args = make_parser.parse_args()
        email = db.email.find_one({'email': args['email']})
        db.account.update({'email': email['_id']},
                          {'$set': {'auth_info': args['auth_info'], 'operator': g.user.username,
                                    'secret': args['secret'], 'operate_status': 1, 'submit_at': datetime.datetime.now()}
                           })
        return {'code': 200, 'msg': 'success'}


# 我的账户
class SelfAccount(Resource):
    @auth.login_required
    def get(self):
        args = proxy_get_parser.parse_args()
        conditions = {'user': g.user.username}
        if args['country']:
            conditions['country'] = args['country']

        def cursor(limit, skip):
            result = db.account.aggregate([{'$match': conditions},
                                           {'$lookup': {'from': 'email', 'localField': 'email', 'foreignField': '_id',
                                                        'as': 'email_info'}},
                                           {'$lookup': {'from': 'address', 'localField': 'address',
                                                        'foreignField': '_id',
                                                        'as': 'address_info'}},
                                           {'$lookup': {'from': 'proxy', 'localField': 'proxy', 'foreignField': '_id',
                                                        'as': 'proxy_info'}},
                                           {'$project': {'email': 0, 'address': 0, 'proxy': 0}},
                                           {'$limit': limit},
                                           {'$skip': skip}
                                           ])
            count = db.account.find({'operate_status': 1}).count()
            return result, count

        page = Page(cursor, args['page'], args['limit'])
        return {'code': 200, 'msg': 'success', 'data': page.page()}

    @auth.login_required
    def post(self):
        args = self_parser.parse_args()
        email = db.email.find_one({'email': args['email']})
        db.account.update({'email': email['_id']}, {'$set': {'can_use': args['can_use']}})
        return {'code': 200, 'msg': 'success'}


# 账户同步
class SyncAccount(Resource):
    def get(self):
        args = sync_parser.parse_args()
        emails = args['email']
        emails = db.email.find({'email': {'$in': emails}})
        results = db.account.find({'email': {'$in': emails}})
        return {'code': 200, 'data': [r for r in results]}

    def post(self):
        pass


# 制作完成的账户
class FinishedAccount(Resource):
    @auth.login_required
    def get(self):
        def cursor(limit, skip):
            result = db.account.aggregate([{'$match': {'operate_status': 1, 'operator': g.user.username}},
                                           {'$lookup': {'from': 'email', 'localField': 'email', 'foreignField': '_id',
                                                        'as': 'email_info'}},
                                           {'$lookup': {'from': 'address', 'localField': 'address',
                                                        'foreignField': '_id',
                                                        'as': 'address_info'}},
                                           {'$lookup': {'from': 'proxy', 'localField': 'proxy', 'foreignField': '_id',
                                                        'as': 'proxy_info'}},
                                           {'$project': {'email': 0, 'address': 0, 'proxy': 0}},
                                           {'$limit': limit},
                                           {'$skip': skip}
                                           ])
            count = db.account.find({'operate_status': 0, 'operator': g.user.username}).count()
            return result, count

        args = proxy_get_parser.parse_args()
        page = Page(cursor, args['page'], args['limit'])
        return {'code': 200, 'msg': 'success', 'data': page.page()}