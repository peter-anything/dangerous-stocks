from datetime import datetime, timedelta

import easyquotation
from django.core.management.base import BaseCommand

from stock.models import Stock, BidHistory, BidSentimentHistory


class BidStatistics(object):
    industry = ''
    count = 0
    total_close_money = 0
    stocks = []

    def __str__(self):
        return '''行业: %s，数量: %s, 包含股票: %s''' % (self.industry, self.count, '###'.join(['%s_%s_%s亿' % (stock['code'], stock['name'], stock['closeMoney']) for stock in self.stocks]))


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        now = datetime.now()
        bid_end_time1 = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                        microseconds=now.microsecond) + timedelta(hours=9, minutes=15, seconds=20)
        bid_end_time2 = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                        microseconds=now.microsecond) + timedelta(hours=9, minutes=20, seconds=20)
        bid_end_time3 = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                        microseconds=now.microsecond) + timedelta(hours=9, minutes=25, seconds=20)
        bid_end_time4 = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                        microseconds=now.microsecond) + timedelta(hours=9, minutes=30, seconds=10)
        if now < bid_end_time1:
            print('当前时间：%s, 时间未到' % now.strftime("%Y-%m-%d %H:%M:%S"))
            return

        if bid_end_time1 <= now < bid_end_time2:
            bids = BidHistory.objects.filter(bidTime__gte=bid_end_time1, bidTime__lt=bid_end_time2)
            if len(bids) > 0:
                print('当前时间：%s, 此时间段已生成数据' % now.strftime("%Y-%m-%d %H:%M:%S"))
                return
        elif bid_end_time2 <= now < bid_end_time3:
            bids = BidHistory.objects.filter(bidTime__gte=bid_end_time2, bidTime__lt=bid_end_time3)
            if len(bids) > 0:
                print('当前时间：%s, 此时间段已生成数据' % now.strftime("%Y-%m-%d %H:%M:%S"))
                return
        elif bid_end_time3 <= now < bid_end_time4:
            bids = BidHistory.objects.filter(bidTime__gte=bid_end_time3, bidTime__lt=bid_end_time4)
            if len(bids) > 0:
                print('当前时间：%s, 此时间段已生成数据' % now.strftime("%Y-%m-%d %H:%M:%S"))
                return
        else:
            bids = BidHistory.objects.filter(bidTime__gte=bid_end_time4)
            if len(bids) > 0:
                print('当前时间：%s, 此时间段已生成数据' % now.strftime("%Y-%m-%d %H:%M:%S"))
                industry_map = {}
                for bid_history in bids:
                    if bid_history.industry in industry_map:
                        industry_map[bid_history.industry].append(bid_history)
                    else:
                        industry_map[bid_history.industry] = [bid_history]
                bid_statistics_arr = []
                for industry, bids in industry_map.items():
                    bid_statistics = BidStatistics()
                    bid_statistics.industry = industry
                    bid_statistics.count = len(bids)
                    total_close_money = 0
                    for bid in bids:
                        total_close_money += bid.bid1Money
                    bid_statistics.stocks = [{
                        'code': bid.code,
                        'name': bid.name,
                        'closeMoney': bid.bid1Money,
                    } for bid in bids]
                    bid_statistics.total_close_money = total_close_money
                    bid_statistics_arr.append(bid_statistics)
                bid_statistics_arr.sort(key=lambda x: (-x.count, -x.total_close_money))
                for bid_statistics in bid_statistics_arr:
                    print(bid_statistics)

        all_stocks = Stock.objects \
            .exclude(code__istartswith='300').exclude(code__istartswith='688').exclude(name__startswith='ST') \
            .filter(market='A股')

        quotation = easyquotation.use('tencent')
        stock_codes = [stock_fundamental.code for stock_fundamental in all_stocks]
        stocks = Stock.objects.filter(code__in=[str(stock_code) for stock_code in stock_codes])
        stock_map = {}
        for stock in stocks:
            stock_map[stock.code] = stock
        real_result = quotation.real([str(stock_code) for stock_code in stock_codes])
        bid_histories = []
        now = datetime.now()
        industry_sentiment_map = {}
        for stock_code, detail in real_result.items():
            bid_price = detail['bid1']
            bid_volume = detail['bid1_volume']
            bid_total = bid_price * bid_volume
            if bid_total >= 50000000:
                bid_history = BidHistory()
                bid_history.code = detail['code']
                bid_history.name = detail['name']
                bid_history.now = detail['now']
                bid_history.open = detail['open']
                bid_history.close = detail['close']

                try:
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
                except Exception as e:
                    print(e)
                    pass

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
