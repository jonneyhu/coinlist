import argparse
import asyncio

# import json
#
# import ccxt
# from ccxt import async_support
#
# key = 'mjlpdje3ld-418fbbdf-b5a6e719-c5367'
# secret = 'fc8add4e-c051ba47-7f75afb9-97d6a'
# proxy = {'http': 'http://127.0.0.1:8889', 'https': 'http://127.0.0.1:8889'}
# hb = ccxt.huobi(
#     {'apiKey': key, 'secret': secret, 'proxies': proxy, 'options': {'createMarketBuyOrderRequiresPrice': False}})
# gateio = ccxt.gateio()
# ok = async_support.okex()
# print(ok.id)
#
# with open('config.json')as f:
#     s = json.load(f)
#     print(s['exchanges'])
# if hb.has['createMarketOrder']:
#     # res = hb.create_market_sell_order('FIL/USDT',1)
#     # print(res)
#     res = hb.create_market_buy_order('FI/USDT', 1, )
#     print('res:', res)
# res = hb.create_limit_buy_order('FIL/USDT',2,76)


# class Argv(object):
#     symbol = None
#     amount = 0
#     price = 0
#     side = 0
#
#
# argv = Argv()
# parser = argparse.ArgumentParser()
# parser.add_argument("symbol", type=str, help='symbol in uppercase', nargs='?')
# parser.add_argument("amount", type=int, default=0, help='coin amount')
# parser.add_argument("price", type=float, default=0, help='coin price')
# parser.add_argument("side", type=int, default=0, help='exchange side 0 is buy 1 is sell')
# parser.parse_args(namespace=argv)
#
#
# async def buy(exchange, symbol, amount, price=0):
#     while 1:
#         try:
#             res = await exchange.create_market_buy_order(symbol, amount)
#             return res
#         except Exception as exits:
#             print(exits)
#
#
# async def sell(exchange, symbol, amount, price=0):
#     pass
#
#
# async def main():
#     exchanges = [['huobi', {}], ['gateio', {}], ['okex', {}]]
#     tasks = []
#     for id in exchanges:
#         exchange = getattr(async_support, id[0])
#         exchang
#         exits = exchange(id[1])
#         if argv.side == 0:  # buy
#             tasks.append(asyncio.ensure_future(buy(exchange, argv.symbol, argv.amount, argv.price)))
#         else:
#             tasks.append(asyncio.ensure_future(sell(exchange, argv.symbol, argv.amount, argv.price)))
#     return await asyncio.gather(*tasks)
#
#
# if __name__ == '__main__':

#     results = asyncio.get_event_loop().run_until_complete(main())
import time
from random import randint, choice

# attribute :石山　树林　矿山　农田　工坊　磨坊　房屋　金矿
import requests

lands = [
    {'coordinates': (-16, 3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-15, 3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-14, 3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-13, 3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-12, 3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-11, 3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-10, 3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-9, 3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-8, 3), 'attribute': ((10, 12), (22, 26), (8, 10), (20, 24))},
    {'coordinates': (-7, 3), 'attribute': ((10, 12), (22, 26), (8, 10), (20, 24))},
    {'coordinates': (-6, 3), 'attribute': ((10, 12), (22, 26), (8, 10), (20, 24))},
    {'coordinates': (-5, 3), 'attribute': ((10, 12), (22, 26), (8, 10), (20, 24))},
    {'coordinates': (-16, 2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-15, 2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-14, 2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-13, 2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-12, 2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-11, 2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-10, 2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-9, 2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-8, 2), 'attribute': ((10, 12), (22, 26), (8, 10), (20, 24))},
    {'coordinates': (-7, 2), 'attribute': ((10, 12), (22, 26), (8, 10), (20, 24))},
    {'coordinates': (-6, 2), 'attribute': ((10, 12), (22, 26), (8, 10), (20, 24))},
    {'coordinates': (-5, 2), 'attribute': ((10, 12), (22, 26), (8, 10), (20, 24))},
    {'coordinates': (-16, 1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-15, 1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-14, 1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-13, 1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-12, 1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-11, 1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-10, 1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-9, 1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-8, 1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-7, 1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-6, 1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-5, 1), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-16, 0), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-15, 0), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-14, 0), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-13, 0), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-12, 0), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-11, 0), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-10, 0), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-9, 0), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-8, 0), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-7, 0), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-6, 0), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-5, 0), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-16, -1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-15, -1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-14, -1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-13, -1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-12, -1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-11, -1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-10, -1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-9, -1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-8, -1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-7, -1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-6, -1), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-5, -1), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-4, -1), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-16, -2), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-15, -2), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-14, -2), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-13, -2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-12, -2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-11, -2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-10, -2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-9, -2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-8, -2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-7, -2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-6, -2), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-5, -2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-4, -2), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-16, -3), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-15, -3), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-14, -3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-13, -3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-10, -3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-9, -3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-7, -3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-6, -3), 'attribute': ((10, 14), (20, 24), (8, 12), (20, 24))},
    {'coordinates': (-5, -3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-4, -3), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-16, -4), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-15, -4), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-14, -4), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-10, -4), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-9, -4), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-7, -4), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-6, -4), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-5, -4), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-4, -4), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-10, -5), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-9, -5), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-7, -5), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-6, -5), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-10, -6), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-9, -6), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},
    {'coordinates': (-6, -6), 'attribute': ((18, 22), (21, 23), (12, 14), (18, 20))},

]
import ipfsApi
import os


class Config:
    """
    配置文件
    """
    data_home = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/'))
    IPFS_url = "61.155.145.110"
    IPFS_port = 5001
    IPFS_port_data = "8080"


api = ipfsApi.Client(Config.IPFS_url, Config.IPFS_port)
all_coordinates = [(x, y) for x in range(10) for y in range(10)]


def create_nft(land, order):
    try:
        nft = {
            'coordinates': (),
            'detail': {'gold': [], 'wood': [], 'workshop': [(4, 3), (5, 3)], 'mill': [(6, 3)],
                       'mine': [], 'farmland': [], 'house': [(5, 5)], 'stone_mountain': [],
                       'empty': [(4, 4), (4, 5), (4, 6), (5, 4), (5, 6), (6, 4), (6, 5), (6, 6)]},
        }
        stone_mountain = land['attribute'][0]
        wood = land['attribute'][1]
        mine = land['attribute'][2]
        farmland = land['attribute'][3]
        stone_mountain_amount = randint(stone_mountain[0], stone_mountain[1])
        wood_amount = randint(wood[0], wood[1])
        mine_amount = randint(mine[0], mine[1])
        farmland_amount = randint(farmland[0], farmland[1])
        print(stone_mountain_amount, mine_amount, farmland_amount, wood_amount)
        r = [(0, 0), (0, 9), (9, 0), (9, 9)]
        # house = [(4, 4), (4, 5), (4, 6), (5, 5)]
        exits = [(4, 4), (4, 5), (4, 6), (5, 4), (5, 6), (6, 4), (6, 5), (6, 6), (5, 5), (4, 3), (5, 3), (6, 3)]
        # 初始化森林和矿山
        while 1:
            init_wood = choice(r)
            if init_wood not in exits:
                exits.append(init_wood)
                break
        r.remove(init_wood)

        while 1:
            init_stone_mountain = choice(r)
            if init_stone_mountain not in exits:
                exits.append(init_stone_mountain)
                break
        r.remove(init_stone_mountain)
        # 初始化矿山农田和金矿
        while 1:
            x = randint(2, 8)
            y = randint(2, 8)
            init_mine = (x, y)
            if init_mine not in exits:
                exits.append(init_mine)
                break
        while 1:
            x = randint(2, 8)
            y = randint(2, 8)
            init_farmland = (x, y)
            if init_farmland not in exits:
                exits.append(init_farmland)
                break
        while 1:
            x = randint(2, 8)
            y = randint(2, 8)
            init_gold = (x, y)
            if init_gold not in exits:
                exits.append(init_gold)
                break

        nft['coordinates'] = land['coordinates']
        # nft['detail']['stone_mountain'].append(init_stone_mountain)
        # nft['detail']['wood'].append(init_wood)
        # nft['detail']['mine'].append(init_mine)
        # nft['detail']['farmland'].append(init_farmland)
        nft['detail']['gold'].append(init_gold)
        # nft['detail']['house'] = house
        # 先确定农田和矿山
        # print(init_farmland, init_mine, init_stone_mountain, init_wood, init_gold)
        self_exits = [init_mine]
        for i in range(0, mine_amount):
            self_exits = list(set(self_exits))
            p = choice(self_exits)
            if i != 0:
                exits.append(p)
            self_exits.remove(p)
            if p[0] + 1 <= 8:
                if (p[0] + 1, p[1]) not in exits:
                    self_exits.append((p[0] + 1, p[1]))
            if p[0] - 1 >= 1:
                if (p[0] - 1, p[1]) not in exits:
                    self_exits.append((p[0] - 1, p[1]))
            if p[1] + 1 <= 8:
                if (p[0], p[1] + 1) not in exits:
                    self_exits.append((p[0], p[1] + 1))
            if p[1] - 1 >= 1:
                if (p[0], p[1] - 1) not in exits:
                    self_exits.append((p[0], p[1] - 1))
            nft['detail']['mine'].append(p)

        self_exits = [init_farmland]
        for i in range(0, farmland_amount):
            self_exits = list(set(self_exits))
            p = choice(self_exits)
            if i != 0:
                exits.append(p)
            self_exits.remove(p)
            if p[0] + 1 <= 8:
                if (p[0] + 1, p[1]) not in exits:
                    self_exits.append((p[0] + 1, p[1]))
            if p[0] - 1 >= 1:
                if (p[0] - 1, p[1]) not in exits:
                    self_exits.append((p[0] - 1, p[1]))
            if p[1] + 1 <= 8:
                if (p[0], p[1] + 1) not in exits:
                    self_exits.append((p[0], p[1] + 1))
            if p[1] - 1 >= 1:
                if (p[0], p[1] - 1) not in exits:
                    self_exits.append((p[0], p[1] - 1))

            nft['detail']['farmland'].append(p)

        # 确定石山和树林
        self_exits = [init_wood]
        for i in range(0, wood_amount):
            self_exits = list(set(self_exits))
            p = choice(self_exits)
            if i != 0:
                exits.append(p)
            self_exits.remove(p)
            if p[0] + 1 <= 9:
                if (p[0] + 1, p[1]) not in exits:
                    self_exits.append((p[0] + 1, p[1]))
            if p[0] - 1 >= 0:
                if (p[0] - 1, p[1]) not in exits:
                    self_exits.append((p[0] - 1, p[1]))
            if p[1] + 1 <= 9:
                if (p[0], p[1] + 1) not in exits:
                    self_exits.append((p[0], p[1] + 1))
            if p[1] - 1 >= 0:
                if (p[0], p[1] - 1) not in exits:
                    self_exits.append((p[0], p[1] - 1))
            nft['detail']['wood'].append(p)

        self_exits = [init_stone_mountain]
        for i in range(0, stone_mountain_amount):
            self_exits = list(set(self_exits))
            p = choice(self_exits)
            if i != 0:
                exits.append(p)
            self_exits.remove(p)
            if p[0] + 1 <= 9:
                if (p[0] + 1, p[1]) not in exits:
                    self_exits.append((p[0] + 1, p[1]))
            if p[0] - 1 >= 0:
                if (p[0] - 1, p[1]) not in exits:
                    self_exits.append((p[0] - 1, p[1]))
            if p[1] + 1 <= 9:
                if (p[0], p[1] + 1) not in exits:
                    self_exits.append((p[0], p[1] + 1))
            if p[1] - 1 >= 0:
                if (p[0], p[1] - 1) not in exits:
                    self_exits.append((p[0], p[1] - 1))
            nft['detail']['stone_mountain'].append(p)

        nft['detail']['river'] = list(set(all_coordinates).difference(set(exits)))
        nft['gold_amount'] = randint(1000, 2000)
        print(nft)
        k = []
        # 石山
        q = '@ '
        # 树林
        w = '# '
        # 矿山
        e = '$ '
        # 农田
        r = '% '
        # 工坊
        t = '^ '
        # 磨坊
        y = '& '
        # 房屋
        u = '* '
        # 金矿
        p = '0 '
        # 河流
        a = '~ '
        # 空地
        b = '  '
        for i in range(10):
            for j in range(10):
                m = [a for z in range(10)]
                for n in nft['detail']['stone_mountain']:
                    if n[1] == i:
                        m[n[0]] = q

                for n in nft['detail']['wood']:
                    if n[1] == i:
                        m[n[0]] = w

                for n in nft['detail']['mine']:
                    if n[1] == i:
                        m[n[0]] = e

                for n in nft['detail']['farmland']:
                    if n[1] == i:
                        m[n[0]] = r

                for n in nft['detail']['workshop']:
                    if n[1] == i:
                        m[n[0]] = t

                for n in nft['detail']['house']:
                    if n[1] == i:
                        m[n[0]] = u

                for n in nft['detail']['gold']:
                    if n[1] == i:
                        m[n[0]] = p

                for n in nft['detail']['mill']:
                    if n[1] == i:
                        m[n[0]] = y
                for n in nft['detail']['empty']:
                    if n[1] == i:
                        m[n[0]] = b

            k.append(m)
        for i in range(len(k)):
            s = "".join(k[i])
            print(s)
        data = {
            "description": "MetaLand is a digital land asset in the Mystar virtual world. With MetaLand, you will be able to create your own planet in Mystar",
            "external_url": "http://www.stardust.social",
            "image": "http://61.155.145.110:8080/ipfs/QmZZgwwzkoxdyBQfr7rHqkJ1FH5akWR16DQx9v7zv6yURD",
            "name": "MetaLand",
            "attributes": [
                {"trait_type": "coordinates", "value": nft['coordinates']},
                {"trait_type": "gold_amount", "value": nft['gold_amount']}
            ],
            'nft': nft
        }
        response = requests.post(url="https://www.stardust.social/api/{0}".format(order), json=data)
        print(response.json())
    except Exception as e:
        create_nft(land, order)


if __name__ == '__main__':
    order = 100
    for land in lands:
        order += 1
        create_nft(land,order)
    # nft = {'coordinates': (11, 22), 'detail': {'gold': [(7, 6)], 'wood': [(9, 0), (9, 1), (8, 1), (7, 1), (8, 0), (9, 2), (7, 2), (9, 3), (8, 2), (7, 0), (7, 0), (9, 4), (9, 5), (8, 2), (7, 3), (9, 6), (8, 3), (7, 4), (8, 0), (9, 7), (7, 5)], 'workshop': [(4, 3), (5, 3)], 'mill': [(6, 3)], 'mine': [(5, 8), (4, 8), (3, 8), (3, 7), (4, 7), (5, 7), (2, 7), (1, 7), (2, 8), (5, 7), (1, 6), (1, 5), (2, 8), (6, 7)], 'farmland': [(2, 3), (1, 3), (1, 4), (1, 2), (2, 4), (2, 2), (2, 5), (3, 3), (3, 4), (2, 6), (3, 5), (2, 4), (1, 1), (2, 1), (2, 1), (3, 4), (3, 5), (2, 2), (3, 6), (3, 2), (4, 2), (3, 1)], 'house': [(5, 5)], 'stone_mountain': [(0, 9), (0, 8), (1, 9), (0, 7), (0, 6), (0, 5), (2, 9), (3, 9), (0, 4), (1, 8), (0, 3), (1, 8), (0, 2), (0, 1), (0, 0), (4, 9), (1, 0), (2, 0), (5, 9), (3, 0)], 'empty': [(4, 4), (4, 5), (4, 6), (5, 4), (5, 6), (6, 4), (6, 5), (6, 6)], 'river': [(4, 0), (5, 1), (8, 9), (9, 8), (8, 6), (6, 2), (7, 7), (6, 8), (5, 0), (8, 5), (8, 8), (6, 1), (7, 9), (4, 1), (5, 2), (8, 4), (9, 9), (8, 7), (6, 0), (6, 9), (7, 8)]}, 'gold_amount': 1767}
    # data = {
    #
    #     "description": "",
    #     "external_url": "https://openseacreatures.io/3",
    #     "image": "http://61.155.145.110:8080/ipfs/QmZk7CWJxKHvHGAxWqg85MoH7Psw5McEgaVdStSEX3yvkH",
    #     "name": "Dave Starbelly",
    #     "attributes": [],
    #     'nft': nft
    # }
    # print(api.add('main.jpg'))
