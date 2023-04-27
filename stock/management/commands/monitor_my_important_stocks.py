import datetime

import easyquotation
from django.core.management.base import BaseCommand

from stock.conf.my_import_stocks import MY_IMPORTANT_STOCKS
from stock.models import Stock, StockStatistics
from stock.util.stock_util import get_stock_statistics_map


class IndustryItem(object):
    industry = ''
    stocks = []

    def __init__(self, industry, stocks):
        self.industry = industry
        self.stocks = stocks


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        now = datetime.datetime.now()

        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond)

        all_stocks = Stock.objects \
            .exclude(code__istartswith='300').exclude(code__istartswith='688').exclude(name__startswith='ST') \
            .exclude(name__startswith='*ST') \
            .filter(market='A股')

        st_name_map = {}
        for st in all_stocks:
            st_name_map[st.name] = st.code

        my_import_codes = []
        quotation = easyquotation.use('tencent')

        stock_statistics_map = get_stock_statistics_map(zero_today, zero_today + datetime.timedelta(hours=16))

        for industry, industry_detail in MY_IMPORTANT_STOCKS.items():
            industry_codes = [st_name_map[name] for name in industry_detail['names']]
            real_result = quotation.real([str(stock_code) for stock_code in industry_codes])

            industry_monitor_stocks = []
            for stock_code, detail in real_result.items():
                code = detail['code']
                name = detail['name']
                now = detail['now']
                open = detail['open']
                close = detail['close']
                high = detail['high']
                low = detail['low']
                bid_price = detail['bid1']

                stock_statistics = stock_statistics_map[code]
                priceMA5 = stock_statistics.priceMA5
                priceMA10 = stock_statistics.priceMA10
                priceMA20 = stock_statistics.priceMA20
                priceMA60 = stock_statistics.priceMA60

                max_up_limit = (now - low) * 100 / low
                if not max_up_limit >= industry_detail['upLimit']:
                    continue

                if now > priceMA5:
                    print('股票：%s, 股价大于5日线' % name)
                elif now > priceMA10:
                    print('股票：%s, 股价大于10日线' % name)
                elif now > priceMA20:
                    print('股票：%s, 股价大于20日线' % name)
                elif now > priceMA60:
                    print('股票：%s, 股价大于60日线' % name)
                else:
                    print('股票：%s, 股价大于60日线' % name)

                industry_monitor_stocks.append(detail)

            if len(industry_monitor_stocks) >= ((len(industry_codes) - 1) / 2 + 1) or len(industry_monitor_stocks) >= 3:
                print('%s 有行情, 包含股票: [%s]' % (industry, [st['name'] for st in industry_monitor_stocks]))
