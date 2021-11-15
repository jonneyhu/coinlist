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
#         except Exception as e:
#             print(e)
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
#         e = exchange(id[1])
#         if argv.side == 0:  # buy
#             tasks.append(asyncio.ensure_future(buy(exchange, argv.symbol, argv.amount, argv.price)))
#         else:
#             tasks.append(asyncio.ensure_future(sell(exchange, argv.symbol, argv.amount, argv.price)))
#     return await asyncio.gather(*tasks)
#
#
# if __name__ == '__main__':
#     results = asyncio.get_event_loop().run_until_complete(main())
from selenium import webdriver
from selenium.webdriver import ChromeOptions

# 1.实例化一个ChromeOptions对象
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

# 2.将ChromeOptions实例化的对象option作为参数传给Crhome对象
path = '/home/jonney/Downloads/chromedriver/chromedriver'
driver = webdriver.Chrome(executable_path=path, options=option)

# 3.发起请求
driver.get('https://coinlist.co/login')