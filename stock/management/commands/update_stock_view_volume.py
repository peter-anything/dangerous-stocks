import datetime

import tushare as ts
from django.core.management.base import BaseCommand
from django_bulk_update.helper import bulk_update

from stock.models import Stock, StockReview
from stock.util import get_stock_type


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        all_stocks = Stock.objects \
            .exclude(code__istartswith='300').exclude(code__istartswith='688').exclude(name__startswith='ST') \
            .exclude(name__startswith='*ST') \
            .filter(market='A股')


        ts.set_token('1c4de25fce18d01933816f3b59c538f55ed362d5ddd23b8c6d4028bf')
        pro = ts.pro_api()
        now = datetime.datetime.now()
        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond) + datetime.timedelta(hours=15)
        all_st_reviews = []
        stock_codes = [stock.code for stock in all_stocks]
        for stock_code in stock_codes:
            print('handle %s' % stock_code)
            try:
                df = pro.daily(ts_code='%s.%s' % (stock_code, get_stock_type(stock_code)), start_date='20230120', end_date='20230202')
                stock_reviews = StockReview.objects.filter(code=stock_code).order_by('-id')[:5]
                i = 0
                for st_review in stock_reviews:
                    st_review.volume = df['vol'][i]
                    st_review.createdAt = zero_today + datetime.timedelta(days=-i)
                    if i == 4:
                        st_review.createdAt = zero_today + datetime.timedelta(days=-13)
                    i += 1
                    all_st_reviews.append(st_review)
            except:
                print(stock_code)
                pass

            if len(all_st_reviews) % 10 == 0:
                bulk_update(all_st_reviews, update_fields=['volume', 'createdAt']) # updates only name column
                all_st_reviews = []

        if len(all_st_reviews) > 0:
            bulk_update(all_st_reviews, update_fields=['volume', 'createdAt']) # updates only name column
