from collections import namedtuple
from datetime import datetime
import json

import requests

try:
    input = raw_input
except:
    pass

StockInfo = namedtuple('StockInfo', [
    'fullname',
    'price',
    'value_changes',
    'percent_changes'
])


def get_stock_info(symbol):
    url = 'https://finance.yahoo.com/quote/' + symbol
    res = requests.get(url)
    res.raise_for_status()

    for line in res.text.split('\n'):
        if 'root.App.main' not in line:
            continue

        data = json.loads(line[16:-1])
        price_info = data['context']['dispatcher']['stores']['QuoteSummaryStore']['price']

        return StockInfo(
            fullname=price_info['longName'] or price_info['shortName'],
            price=price_info['regularMarketPrice']['raw'],
            value_changes=price_info['regularMarketChange']['raw'],
            percent_changes=price_info['regularMarketChangePercent']['raw']
        )


def print_stock_info(info):
    print(datetime.now())
    print(info.fullname)
    print('{:,.2f} {} ({}%)'.format(info.price, prepend_unary(info.value_changes), prepend_unary(info.percent_changes)))
    print('')


def prepend_unary(n):
    prefix = '+' if n >= 0 else ''
    return prefix + '{:,.2f}'.format(n)


def main():
    while True:
        symbol = input('Please enter a symbol: ').strip()
        if symbol == ':q':
            break

        try:
            stock_info = get_stock_info(symbol)
        except:
            print('Failed to retrieve information for symbol ' + symbol)
            continue

        print_stock_info(stock_info)

    print('END')


if __name__ == '__main__':
    main()

