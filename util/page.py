import math

from mongoengine.base import BaseField

from model.user import User


class Page():

    def __init__(self,queryset,current_page,limit):
        self.total = queryset.count()
        self.queryset = queryset
        self.pages = math.ceil(self.total/limit)
        skip = (current_page-1)*limit
        self.data = self.queryset.limit(limit).skip(skip)
        print(self.data)


    def page(self):
        data=[]
        for result in self.data:
            del result['_id']
            data.append(result)
        return {'pages': self.pages, 'total': self.total, 'data': data}


