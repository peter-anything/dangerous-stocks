import csv
import datetime

from django.core.management.base import BaseCommand, CommandError

import easyquotation

from stock.models import Stock, StockFundamental


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        all_stock_fundamentals = StockFundamental.objects.filter(createdAt__gte=datetime.datetime.now() + datetime.timedelta(days=-1))
        all_stack_codes = [stock_fundamental.code for stock_fundamental in all_stock_fundamentals]
        all_stock_map = {}
        for code in all_stack_codes:
            all_stock_map[code] = True
        now = datetime.datetime.now()
        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond) + datetime.timedelta(hours=15)

        stock_codes = []
        with open('all_stock_codes.txt', encoding='utf-8') as f:
            for line in f:
                values = line.split()
                if values:
                    code = values[0].strip()
                    stock_codes.append(code)

        quotation = easyquotation.use('tencent')
        stock_fundamentals = []
        for i in range(6):
            curr_stock_codes = stock_codes[i * 1000:(i + 1) * 1000]
            real_result = quotation.real(curr_stock_codes)

            for stock_code, detail in real_result.items():
                stockFundamental = StockFundamental()
                stockFundamental.code = detail['code']
                stockFundamental.name = detail['name']
                stockFundamental.marketValue = detail['总市值']
                stockFundamental.tradingMarketValue = detail['流通市值']
                stockFundamental.turnoverRate = detail['turnover']
                stockFundamental.open = detail['open']
                stockFundamental.tradingMoney = detail['成交量(手)']
                stockFundamental.turnoverVolume = detail['成交额(万)']
                stockFundamental.high = detail['high']
                stockFundamental.low = detail['low']
                stockFundamental.close = detail['now']
                stockFundamental.pe = detail['PE']
                stockFundamental.createdAt = zero_today
                if detail['open'] > 0 and detail['close'] > 0:
                    stockFundamental.growthRate = (detail['close'] - detail['open']) * 100 / detail['open']
                stock_fundamentals.append(stockFundamental)

        StockFundamental.objects.bulk_create(stock_fundamentals)

