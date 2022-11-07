import csv

from django.core.management.base import BaseCommand, CommandError

import easyquotation

from stock.models import Stock, StockFundamental


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        with open('stock.csv', encoding='utf-8') as f:
            f_csv = csv.reader(f)
            for idx, line in enumerate(f_csv):
                if idx == 0:
                    continue
                print(line[0])
                quotation = easyquotation.use('tencent')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
                real_result = quotation.real([str(line[0])])
                print(real_result)
                stock = Stock()
                for stock_code, detail in real_result.items():
                    stock.code = detail['code']
                    stock.name = detail['name']
                    stock.marketValue = detail['总市值']
                    stock.tradingMarketValue = detail['流通市值']
                    stock.turnoverRate = detail['turnover']
                    stock.open = detail['open']
                    stock.high = detail['high']
                    stock.low = detail['low']
                    stock.pe
                stock.save()

    def handle(self, *args, **options):
        code_set = set()

        stock_fundamentals = []
        stocks = []
        idx = 0
        with open('stock.csv', encoding='utf-8') as f:
            f_csv = csv.reader(f)
            for idx, line in enumerate(f_csv):
                if idx == 0:
                    continue
                if line[0] in code_set:
                    continue

                code_set.add(line[0])

                stock = Stock()
                stock.code = line[0]
                stock.name = line[1]
                stock.market = line[2]
                stock.category = line[3]
                stock.type = line[4]
                stocks.append(stock)

                idx += 1
                if idx % 1000 == 0:
                    quotation = easyquotation.use('tencent')
                    real_result = quotation.real([str(stock.code) for stock in stocks])
                    for stock_code, detail in real_result.items():
                        stockFundamental = StockFundamental()
                        stockFundamental.code = detail['code']
                        stockFundamental.name = detail['name']
                        stockFundamental.marketValue = detail['总市值']
                        stockFundamental.tradingMarketValue = detail['流通市值']
                        stockFundamental.turnoverRate = detail['turnover']
                        stockFundamental.open = detail['open']
                        stockFundamental.high = detail['high']
                        stockFundamental.low = detail['low']
                        stockFundamental.pe = detail['PE']
                        stock_fundamentals.append(stockFundamental)
                    StockFundamental.objects.bulk_create(stock_fundamentals)
                    stock_fundamentals = []
        if len(stock_fundamentals) > 0:
            StockFundamental.objects.bulk_create(stock_fundamentals)
