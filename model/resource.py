import mongoengine as me
import math



class Email(me.Document):
    address = me.StringField(required=True)
    password = me.StringField(required=True)
    assist = me.StringField()
    is_used = me.BooleanField()
    belong = me.StringField()


class Address(me.Document):
    address = me.StringField(required=True)
    postcode = me.StringField(required=True)
    is_used = me.BooleanField()
    country = me.StringField(required=True)


class Proxy(me.Document):
    server = me.StringField(required=True)
    origin_ip = me.StringField(required=True)
    times = me.IntField(default=0)
    country = me.StringField(required=True)