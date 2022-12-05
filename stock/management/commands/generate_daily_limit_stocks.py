import datetime

import easyquotation
from django.core.management.base import BaseCommand

from stock.models import Stock, DailyLimitLevel1Stock, DailyLimitLevel2Stock


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        all_stocks = Stock.objects \
            .exclude(code__istartswith='300').exclude(code__istartswith='688').exclude(name__startswith='ST') \
            .filter(market='A股')

        now = datetime.datetime.now()
        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, days=-1,
                                              microseconds=now.microsecond) + datetime.timedelta(hours=15)

        quotation = easyquotation.use('tencent')
        stock_codes = [stock_fundamental.code for stock_fundamental in all_stocks]
        stocks = Stock.objects.filter(code__in=[str(stock_code) for stock_code in stock_codes])
        stock_map = {}
        for stock in stocks:
            stock_map[stock.code] = stock
        real_result = quotation.real([str(stock_code) for stock_code in stock_codes])
        bid_histories = []
        now = datetime.datetime.now()
        industry_sentiment_map = {}
        daily_limit_level1_stocks = []
        daily_limit_level2_stocks = []
        daily_limit_level3_stocks = []
        for stock_code, detail in real_result.items():
            code = detail['code']
            name = detail['name']
            now = detail['now']
            open = detail['open']
            close = detail['close']
            bid_price = detail['bid1']
            if open > 0 and close > 0:
                grow_rate = (now - close) * 100 / open
                if grow_rate > 9:
                    print('%s_%s' % (code, name))

                    daily_limit_stock = DailyLimitLevel1Stock()
                    daily_limit_stock.code = code
                    daily_limit_stock.name = name
                    daily_limit_stock.open = open
                    daily_limit_stock.close = close
                    daily_limit_stock.now = now
                    daily_limit_stock.buyPrice = close
                    daily_limit_stock.buyReason = '打板'
                    daily_limit_stock.buyDate = zero_today
                    daily_limit_stock.safePrice = close
                    daily_limit_stock.lowestPrice = close
                    daily_limit_stock.industry = stock_map[code].industry
                    daily_limit_stock.concepts = stock_map[code].concepts
                    daily_limit_stock.type = stock_map[code].type
                    daily_limit_stock.growthRate = grow_rate
                    daily_limit_stock.highestPrice = now
                    print(stock_map[code].industry)
                    print(stock_map[code].concepts)
                    print(stock_map[code].type)
                    daily_limit_level1_stocks.append(daily_limit_stock)
                elif grow_rate >= 3:
                    daily_limit_stock = DailyLimitLevel2Stock()
                    daily_limit_stock.code = code
                    daily_limit_stock.name = name
                    daily_limit_stock.open = open
                    daily_limit_stock.close = close
                    daily_limit_stock.now = now
                    daily_limit_stock.buyPrice = close
                    daily_limit_stock.buyReason = '追涨'
                    daily_limit_stock.buyDate = zero_today
                    daily_limit_stock.safePrice = close
                    daily_limit_stock.lowestPrice = close
                    daily_limit_stock.highestPrice = now
                    daily_limit_stock.industry = stock_map[code].industry
                    daily_limit_stock.concepts = stock_map[code].concepts
                    daily_limit_stock.type = stock_map[code].type
                    daily_limit_stock.growthRate = grow_rate
                    print(stock_map[code].industry)
                    print(stock_map[code].concepts)
                    print(stock_map[code].type)
                    daily_limit_level2_stocks.append(daily_limit_stock)


        DailyLimitLevel1Stock.objects.bulk_create(daily_limit_level1_stocks)
        DailyLimitLevel2Stock.objects.bulk_create(daily_limit_level2_stocks)