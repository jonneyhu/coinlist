import datetime
import math
import json

from bson import ObjectId



class JSONEncoder(json.JSONEncoder):
    '''处理ObjectId,该类型无法转为json'''
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return datetime.datetime.strftime(o,'%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, o)


class Page():

    def __init__(self,queryset,current_page,limit):
        skip = (current_page - 1) * limit
        if callable(queryset):
            result,count = queryset(limit,skip)
            queryset = [i for i in result]
            self.total = count
            self.pages = math.ceil(self.total / limit)
            self.data = queryset
        else:
            self.total = queryset.count()
            self.pages = math.ceil(self.total/limit)
            self.data = queryset.limit(limit).skip(skip)



    def page(self):
        data=[]
        for result in self.data:
            del result['_id']
            result = json.loads(JSONEncoder().encode(result))
            data.append(result)

        return {'pages': self.pages, 'total': self.total, 'data': data}


