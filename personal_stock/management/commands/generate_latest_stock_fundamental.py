import csv
import datetime

from django.core.management.base import BaseCommand, CommandError

import easyquotation

from personal_stock.models import Stock, StockFundamental


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):

        all_stock_fundamentals = StockFundamental.objects.filter(createdAt__gte=datetime.datetime.now() + datetime.timedelta(days=-1))
        all_stack_codes = [stock_fundamental.code for stock_fundamental in all_stock_fundamentals]
        all_stock_map = {}
        for code in all_stack_codes:
            all_stock_map[code] = True
        with open('all_stock_codes.txt', encoding='utf-8') as f:
            quotation = easyquotation.use('tencent')
            stock_fundamentals = []
            idx = 0
            for line in f:
                values = line.split()
                if values:
                    code = values[0].strip()
                    if code in all_stock_map:
                        print('already exists: %s' % code)
                    else:
                        continue
                    real_result = quotation.real([str(code)])
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
                        stockFundamental.createdAt = datetime.datetime.now()
                        stock_fundamentals.append(stockFundamental)

                    idx = idx + 1
                    if idx % 100 == 0:
                        StockFundamental.objects.bulk_create(stock_fundamentals)
                        stock_fundamentals = []
            if len(stock_fundamentals) > 0:
                StockFundamental.objects.bulk_create(stock_fundamentals)