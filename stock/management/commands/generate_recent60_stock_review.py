import datetime

import easyquotation
from django.core.management.base import BaseCommand

from stock.models import Stock, StockReview, StockReviewRecent60


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        all_stocks = Stock.objects \
            .exclude(code__istartswith='300').exclude(code__istartswith='688').exclude(name__startswith='ST') \
            .exclude(name__startswith='*ST') \
            .filter(market='A股')

        now = datetime.datetime.now()

        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond)

        # 午盘
        mid_day = zero_today + datetime.timedelta(hours=12, minutes=59)

        late_day = zero_today + datetime.timedelta(hours=15)

        curr_day = late_day
        if now < mid_day:
            curr_day = mid_day

        quotation = easyquotation.use('tencent')
        stock_codes = [stock_fundamental.code for stock_fundamental in all_stocks]
        stocks = Stock.objects.filter(code__in=[str(stock_code) for stock_code in stock_codes])
        stock_map = {}
        for stock in stocks:
            stock_map[stock.code] = stock
        real_result = quotation.real([str(stock_code) for stock_code in stock_codes])
        now = datetime.datetime.now()
        stock_review_arr = []
        for stock_code, detail in real_result.items():
            code = detail['code']
            name = detail['name']
            now = detail['now']
            open = detail['open']
            close = detail['close']
            high = detail['high']
            low = detail['low']
            bid_price = detail['bid1']
            #    upLimitType = models.IntegerField() # 1、 涨停 2、 跌停 3、上涨 4、下跌 5、平
            if open > 0 and close > 0:
                grow_rate = (now - close) * 100 / close

                stock_review = StockReviewRecent60()
                stock_review.code = code
                stock_review.name = name
                stock_review.open = open
                stock_review.close = close
                stock_review.high = high
                stock_review.low = low
                stock_review.now = now
                stock_review.createdAt = curr_day
                stock_review.marketValue = detail['总市值']
                stock_review.volume = detail['成交量(手)']
                stock_review.tradingMarketValue = detail['流通市值']
                stock_review.turnoverRate = detail['turnover']
                stock_review.pe = detail['PE']
                stock_review.upLimit = detail['涨停价']
                stock_review.downLimit = detail['跌停价']

                if 3 >= grow_rate >= 1:
                    stock_review.smallUp = 1

                stock_review.everUpLimited = 0

                if -0.000001 <= stock_review.upLimit - stock_review.now <= 0.000001:
                    stock_review.upLimitType = 1
                else:
                    if -0.000001 <= stock_review.downLimit - stock_review.now <= 0.000001:
                        stock_review.upLimitType = 2
                    elif grow_rate > 0:
                        stock_review.upLimitType = 3
                    elif grow_rate < 0:
                        stock_review.upLimitType = 4
                    elif grow_rate == 0:
                        stock_review.upLimitType = 5

                    if -0.000001 <= stock_review.upLimit - stock_review.high <= 0.000001:
                        stock_review.everUpLimited = 1

                stock_review.industry = stock_map[code].industry
                stock_review.concepts = stock_map[code].concepts
                stock_review.type = stock_map[code].type
                stock_review.growthRate = grow_rate
                stock_review.bid1Money = detail['bid1'] * detail['bid1_volume'] / 10000000
                stock_review_arr.append(stock_review)

        StockReviewRecent60.objects.bulk_create(stock_review_arr)
