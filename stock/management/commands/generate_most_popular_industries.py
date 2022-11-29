import csv
import datetime

from django.core.management.base import BaseCommand, CommandError

import easyquotation

from stock.models import Stock, StockFundamental, BidHistory, BidSentimentHistory


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        all_stock_fundamentals = StockFundamental.objects\
            .filter(createdAt__gte=datetime.datetime.now() + datetime.timedelta(days=-1)) \
            .exclude(code__istartswith='300').exclude(code__istartswith='688').exclude(name__startswith='ST')

        quotation = easyquotation.use('tencent')
        stock_codes = [stock_fundamental.code for stock_fundamental in all_stock_fundamentals]
        stocks = Stock.objects.filter(code__in=[str(stock_code) for stock_code in stock_codes])
        stock_map = {}
        for stock in stocks:
            stock_map[stock.code] = stock
        real_result = quotation.real([str(stock_code) for stock_code in stock_codes])
        bid_histories = []
        now = datetime.datetime.now()
        industry_sentiment_map = {}
        for stock_code, detail in real_result.items():
            bid_price = detail['bid1']
            bid_volume = detail['bid1_volume']
            bid_total = bid_price * bid_volume
            if bid_total >= 5000 * 10000:
                bid_history = BidHistory()
                bid_history.code = detail['code']
                bid_history.name = detail['name']
                bid_history.now = detail['now']
                bid_history.open = detail['open']
                bid_history.close = detail['close']
                if (bid_history.open - bid_history.close) * 100 / bid_history.close > 9:
                    bid_history.openHigh = 1
                elif (bid_history.open - bid_history.close) * 100 / bid_history.close > 5:
                    bid_history.openHigh = 2
                elif (bid_history.open - bid_history.close) * 100 / bid_history.close > 3:
                    bid_history.openHigh = 3
                else:
                    bid_history.openHigh = 4

                bid_history.bidTime = now
                bid_history.bid1Money = detail['bid1'] * detail['bid1_volume'] / 10000000
                bid_history.bid2Money = detail['bid2'] * detail['bid2_volume'] / 10000000
                bid_history.bid3Money = detail['bid3'] * detail['bid3_volume'] / 10000000
                bid_history.bid4Money = detail['bid4'] * detail['bid4_volume'] / 10000000
                bid_history.bid5Money = detail['bid5'] * detail['bid5_volume'] / 10000000
                bid_history.industry = stock_map[detail['code']].industry
                bid_history.concepts = stock_map[detail['code']].concepts
                bid_history.type = stock_map[detail['code']].type

                if bid_history.industry in industry_sentiment_map:
                    industry_sentiment_map[bid_history.industry] += 1
                else:
                    industry_sentiment_map[bid_history.industry] = 1

                bid_histories.append(
                    bid_history
                )
        BidHistory.objects.bulk_create(bid_histories)

        bid_sentiment_histories = []
        for industry, count in industry_sentiment_map.items():
            bid_sentiment_history = BidSentimentHistory()
            bid_sentiment_history.bidTime = now
            bid_sentiment_history.industry = industry
            bid_sentiment_history.count = count
            bid_sentiment_histories.append(bid_sentiment_history)

        BidSentimentHistory.objects.bulk_create(bid_sentiment_histories)
