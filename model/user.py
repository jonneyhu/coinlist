from hashlib import md5
import mongoengine as me
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from application import app

class User(me.Document):
    username = me.StringField(required=True)
    password = me.StringField()
    level = me.IntField(default=0)

    def keys(self):
        return ('username','level')

    def __getitem__(self, item):
        return getattr(self,item)

    def set_password(self, password):
        h = md5(password.encode('utf8'))
        self.password = h.hexdigest()

    def verify_password(self,password):
        if self.password == md5(password.encode('utf8')).hexdigest():
            return True
        return False

    def generate_token(self):
        # 实例化一个签名序列化对象 serializer，有效期 10 分钟
        serializer = Serializer(app.config['SECRET_KEY'], expires_in=3600*24*15)
        token = serializer.dumps({'username':self.username})
        return token.decode()