from datetime import timedelta, datetime

import easyquotation
from bulk_update.helper import bulk_update
from django.core.management.base import BaseCommand

from stock.models import ManualRecommendStock, ManualRecommendStockPriceHistory


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        stocks = ManualRecommendStock.objects.filter(cancel=0)
        print(stocks.query)
        stock_codes = [stock.code for stock in stocks]

        quotation = easyquotation.use('tencent')
        now = datetime.now()

        real_result = quotation.real([str(stock_code) for stock_code in stock_codes])
        manual_recommend_stock_price_history_arr = []

        now = datetime.now()
        bid_end_time4 = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                        microseconds=now.microsecond) + timedelta(hours=9, minutes=30, seconds=10)
        after_half_hour_time = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                               microseconds=now.microsecond) + timedelta(hours=10, minutes=00,
                                                                                         seconds=0)
        is_after_half_hour = now >= after_half_hour_time
        close_time = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                     microseconds=now.microsecond) + timedelta(hours=15, minutes=00, seconds=10)

        manual_recommend_stock_price_histories = ManualRecommendStockPriceHistory.objects.filter(
            createdAt__gt=bid_end_time4)
        exists_codes = [manual_recommend_stock_price_history.code for manual_recommend_stock_price_history in
                        manual_recommend_stock_price_histories]

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
            downRate = (low - close) * 100 / open
            riseUpRate = (high - close) * 100 / open
            nowRate = (now_price - close) * 100 / open
            close_rate = (now_price - close) * 100 / open
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
                                   'now'])  # updates only name column
