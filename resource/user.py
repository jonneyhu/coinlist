from _md5 import md5

from flask_restful import Resource, reqparse

from application import app
from model.user import User
from flask_httpauth import HTTPTokenAuth
from flask import g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

auth = HTTPTokenAuth(scheme='Token')
serializer = Serializer(app.config['SECRET_KEY'], expires_in=3600*24*15)


# 认证回调函数
@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = serializer.loads(token)
    except:
        return False
    if 'username' in data:
        g.user = User.objects(username=data['username']).first()
        return True
    return False


parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)


class UserResource(Resource):
    def get(self):
        pass

    def post(self):
        user = User(username='jonney')
        user.set_password("123456")
        user.save()
        return {'code': 200, 'msg': 'success'}


class Login(Resource):
    def get(self):
        args = parser.parse_args()
        password = md5(args['password'].encode('utf8')).hexdigest()
        user = User.objects(username=args['username'], password=password).first()
        return {'code': 200, 'data': user.generate_token()}

