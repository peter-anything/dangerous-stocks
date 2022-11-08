import csv
import datetime

import tushare as ts
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

    def get_all_stock_detail(self, stock_codes, duration):
        stock_codes = stock_codes
        query_date = (datetime.datetime.now() + datetime.timedelta(duration)).strftime('%Y%m%d')
        query_stocks = ','.join([self.get_query_ts_code(code) for code in stock_codes])
        df = self.pro.daily(ts_code=query_stocks, start_date=query_date,
                            end_date=query_date)

        return df

    def generate_data(self, duration):
        now = datetime.datetime.now()
        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond)
        last_today = zero_today + datetime.timedelta(hours=23, minutes=59, seconds=59)

        stock_codes = []
        with open('all_stock_codes.txt', encoding='utf-8') as f:
            for line in f:
                values = line.split()
                if values:
                    code = values[0].strip()
                    stock_codes.append(code)
        print(len(stock_codes))

        with open((now + datetime.timedelta(duration)).strftime('%Y-%m-%d') + '.csv', 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow([
                'ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol',
                'amount'
            ])
            for i in range(6):
                curr_stock_codes = stock_codes[i * 1000:(i + 1) * 1000]
                df = self.get_all_stock_detail(curr_stock_codes, duration)
                for index, row in df.iterrows():
                    ts_code, trade_date, iopen, high, low, close, pre_close, change, pct_chg, vol, amount = \
                        row.get(0)[0:-3], row.get(1), row.get(2), row.get(3), row.get(4), row.get(5), row.get(
                            6), row.get(7), row.get(8), row.get(9), row.get(10)
                    f_csv.writerow([ts_code, trade_date, iopen, high, low, close, pre_close, change, pct_chg, vol, amount])

    def save_to_db(self, duration):
        now = datetime.datetime.now()
        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond)
        stocks = Stock.objects.all()
        stock_map = {}
        for stock in stocks:
            stock_map[stock.code] = stock.name
        stock_fundamentals = []
        with open((now + datetime.timedelta(duration)).strftime('%Y-%m-%d') + '.csv', 'r') as f:
            f_csv = csv.reader(f)
            for idx, row in enumerate(f_csv):
                if idx == 0: continue
                ts_code, trade_date, iopen, high, low, close, pre_close, change, pct_chg, vol, amount = row
                stockFundamental = StockFundamental()
                stockFundamental.code = ts_code
                stockFundamental.name = stock_map[ts_code]
                # stockFundamental.marketValue = detail['总市值']
                # stockFundamental.tradingMarketValue = detail['流通市值']
                # stockFundamental.turnoverRate = detail['turnover']
                stockFundamental.open = iopen
                stockFundamental.high = high
                stockFundamental.low = low
                stockFundamental.close = close
                # stockFundamental.pe = detail['PE']
                stockFundamental.createdAt = zero_today + datetime.timedelta(duration) + datetime.timedelta(hours=15)
                stock_fundamentals.append(stockFundamental)
        StockFundamental.objects.bulk_create(stock_fundamentals)


    def handle(self, *args, **options):
        # self.generate_data(0)
        # self.generate_data(-1)
        self.save_to_db(-1)