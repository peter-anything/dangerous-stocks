from datetime import datetime, timedelta

import easyquotation
from bulk_update.helper import bulk_update

from stock.models import Stock, BidHistory, BidSentimentHistory, ManualRecommendStock, ManualRecommendStockPriceHistory


class BidStatistics(object):
    industry = ''
    count = 0
    total_close_money = 0
    stocks = []

    def __str__(self):
        return '''行业: %s，数量: %s, 包含股票: %s''' % (self.industry, self.count, '###'.join(
            ['%s_%s_%s亿' % (stock['code'], stock['name'], stock['closeMoney']) for stock in self.stocks]))


def generate_most_popular_industries():
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
            print('##################################################################')
            for bid_statistics in bid_statistics_arr:
                print(bid_statistics)
            print('##################################################################')
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
            print('##################################################################')
            for bid_statistics in bid_statistics_arr:
                print(bid_statistics)
            print('##################################################################')
            return

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
        if bid_total >= 5000 * 10000:
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


def generate_manual_recommend_stock_price_history():
    now = datetime.now()
    bid_end_time4 = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                    microseconds=now.microsecond) + timedelta(hours=9, minutes=30, seconds=10)
    after_half_hour_time = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                           microseconds=now.microsecond) + timedelta(hours=10, minutes=00,
                                                                                     seconds=0)
    close_time = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                 microseconds=now.microsecond) + timedelta(hours=15, minutes=00, seconds=10)
    if now < bid_end_time4:
        print('当前时间：%s, 未开盘，不操作' % now.strftime("%Y-%m-%d %H:%M:%S"))
        return

    if now > close_time:
        print('当前时间：%s, 已闭盘，不操作' % now.strftime("%Y-%m-%d %H:%M:%S"))
        return

    manual_recommend_stock_price_histories = ManualRecommendStockPriceHistory.objects.filter(
        createdAt__gt=bid_end_time4)
    exists_codes = [manual_recommend_stock_price_history.code for manual_recommend_stock_price_history in
                    manual_recommend_stock_price_histories]

    stocks = ManualRecommendStock.objects.filter(cancel=0)
    stock_codes = [stock.code for stock in stocks]

    quotation = easyquotation.use('tencent')
    now = datetime.now()

    real_result = quotation.real([str(stock_code) for stock_code in stock_codes])

    not_in_db_codes = set(stock_codes) - set(exists_codes)
    if len(not_in_db_codes) > 0:
        tmp_manual_recommend_stock_price_history_arr = []
        for not_in_db_code in not_in_db_codes:
            detail = real_result[not_in_db_code]
            manual_recommend_stock_price_history = ManualRecommendStockPriceHistory()
            manual_recommend_stock_price_history.code = detail['code']
            manual_recommend_stock_price_history.name = detail['name']
            manual_recommend_stock_price_history.open = detail['open']
            manual_recommend_stock_price_history.close = detail['close']
            manual_recommend_stock_price_history.low = detail['low']
            manual_recommend_stock_price_history.high = detail['high']
            manual_recommend_stock_price_history.createdAt = now
            manual_recommend_stock_price_history.marketValue = detail['总市值']
            manual_recommend_stock_price_history.tradingMarketValue = detail['流通市值']
            manual_recommend_stock_price_history.turnoverRate = detail['turnover']
            manual_recommend_stock_price_history.pe = detail['PE']
            manual_recommend_stock_price_history.bid1Money = detail['bid1'] * detail['bid1_volume'] / 10000000
            openHighRate = (
                                   manual_recommend_stock_price_history.open - manual_recommend_stock_price_history.close) * 100 / manual_recommend_stock_price_history.close
            if openHighRate > 9:
                manual_recommend_stock_price_history.openHigh = 1
            elif openHighRate > 5:
                manual_recommend_stock_price_history.openHigh = 2
            elif openHighRate > 3:
                manual_recommend_stock_price_history.openHigh = 3
            else:
                manual_recommend_stock_price_history.openHigh = 4
            manual_recommend_stock_price_history.openHighRate = openHighRate
            manual_recommend_stock_price_history.alertRate = openHighRate
            tmp_manual_recommend_stock_price_history_arr.append(manual_recommend_stock_price_history)
        ManualRecommendStockPriceHistory.objects.bulk_create(tmp_manual_recommend_stock_price_history_arr)
        manual_recommend_stock_price_histories = ManualRecommendStockPriceHistory.objects.filter(
            createdAt__gt=bid_end_time4)

    manual_recommend_stock_price_history_map = {}
    for manual_recommend_stock_price_history in manual_recommend_stock_price_histories:
        manual_recommend_stock_price_history_map[
            manual_recommend_stock_price_history.code] = manual_recommend_stock_price_history

    for stock_code, detail in real_result.items():
        db_low = manual_recommend_stock_price_history_map[stock_code].low
        db_high = manual_recommend_stock_price_history_map[stock_code].high
        low = detail['low']
        high = detail['high']
        open = detail['open']
        now_price = detail['now']
        close = detail['close']
        if low < db_low:
            manual_recommend_stock_price_history_map[stock_code].low = low
        if high > db_high:
            manual_recommend_stock_price_history_map[stock_code].high = high
        if open <= 0:
            continue
        downRate = (low - close) * 100 / close
        riseUpRate = (high - close) * 100 / close
        nowRate = (now_price - close) * 100 / close
        close_rate = (now_price - close) * 100 / close
        manual_recommend_stock_price_history_map[stock_code].downRate = downRate
        manual_recommend_stock_price_history_map[stock_code].riseUpRate = riseUpRate
        manual_recommend_stock_price_history_map[stock_code].nowRate = nowRate
        manual_recommend_stock_price_history_map[stock_code].now = now_price

        if now >= close_time:
            manual_recommend_stock_price_history_map[stock_code].closeRate = close_rate

        if now >= after_half_hour_time:
            if not manual_recommend_stock_price_history_map[stock_code].afterHalfHourNowRate:
                manual_recommend_stock_price_history_map[stock_code].afterHalfHourNowRate = nowRate
            if not manual_recommend_stock_price_history_map[stock_code].afterHalfHourDownRate:
                manual_recommend_stock_price_history_map[stock_code].afterHalfHourDownRate = downRate
            if not manual_recommend_stock_price_history_map[stock_code].afterHalfHourRiseUpRate:
                manual_recommend_stock_price_history_map[stock_code].afterHalfHourRiseUpRate = riseUpRate

        if riseUpRate >= 3 * 0.9:
            manual_recommend_stock_price_history_map[stock_code].needAlert = 1

    bulk_update(manual_recommend_stock_price_histories,
                update_fields=['high', 'low', 'downRate', 'riseUpRate',
                               'nowRate', 'needAlert', 'closeRate', 'afterHalfHourNowRate',
                               'afterHalfHourDownRate', 'afterHalfHourRiseUpRate',
                               'now'])
