import datetime

import tushare as ts
from bulk_update.helper import bulk_update
from django.core.management.base import BaseCommand

from stock.models import StockFundamental, Stock


class Command(BaseCommand):
    help = 'test'

    def __init__(self):
        ts.set_token('a0c72739321030db33cfdf7a885ea990bc95ee6a4165265273c212e2')
        self.pro = ts.pro_api()

    def get_stock_type(self, stock_code):
        """判断股票ID对应的证券市场
        匹配规则
        ['50', '51', '60', '90', '110'] 为 sh
        ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
        ['5', '6', '9'] 开头的为 sh， 其余为 sz
        :param stock_code:股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
        :return 'sh' or 'sz'"""
        assert type(stock_code) is str, "stock code need str type"
        sh_head = ("50", "51", "60", "90", "110", "113", "118",
                   "132", "204", "5", "6", "9", "7")
        return "SH" if stock_code.startswith(sh_head) else "SZ"

    def get_query_ts_code(self, stock_code):
        return '%s.%s' % (stock_code, self.get_stock_type(stock_code))

    def get_stock_detail(self, stock_code):
        df = self.pro.daily(ts_code='%s.%s' % (stock_code, self.get_stock_type(stock_code)), start_date='20221107',
                            end_date='20221107')

        return df

    def get_all_stock_detail(self, stock_codes, duration):
        stock_codes = stock_codes
        query_date = (datetime.datetime.now() + datetime.timedelta(duration)).strftime('%Y%m%d')
        query_stocks = ','.join([self.get_query_ts_code(code) for code in stock_codes])
        df = self.pro.daily(ts_code=query_stocks, start_date=query_date,
                            end_date=query_date)

        return df

    def update_by_day(self, duration):
        now = datetime.datetime.now()
        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond)
        last_today = zero_today + datetime.timedelta(hours=23, minutes=59, seconds=59)
        all_stock_fundamentals = StockFundamental.objects.filter(
            createdAt__gte=zero_today + datetime.timedelta(days=duration),
            createdAt__lte=last_today + datetime.timedelta(days=duration)
            )
        print(all_stock_fundamentals.query)
        count = len(all_stock_fundamentals)
        stock_fundamental_map = {}
        for stock_fundamental in all_stock_fundamentals:
            stock_fundamental_map[stock_fundamental.code] = stock_fundamental
        stock_codes = [stock_fundamental.code for stock_fundamental in all_stock_fundamentals]
        for i in range(10):
            curr_stock_codes = stock_codes[i * 1000:(i+1) * 1000]
            df = self.get_all_stock_detail(curr_stock_codes, duration)
            for index, row in df.iterrows():
                ts_code, trade_date, iopen, high, low, close, pre_close, change, pct_chg, vol, amount = \
                    row.get(0)[0:-3], row.get(1), row.get(2), row.get(3), row.get(4), row.get(5), row.get(
                        6), row.get(7), row.get(8), row.get(9), row.get(10)
                if stock_fundamental_map.get(ts_code):
                    stock_fundamental_map[ts_code].close = close
                # StockFundamental.objects.filter(code=ts_code).update(close=close)
        bulk_update(all_stock_fundamentals, update_fields=['close'])  # updates only name column

    def handle(self, *args, **options):
        self.update_by_day(0)
        # self.update_by_day(-1)
        # self.update_by_day(-2)