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
        akshare_today = now.strftime("%Y%m%d")
        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond) + datetime.timedelta(hours=15)
        all_st_reviews = []
        stock_codes = [stock.code for stock in all_stocks]
        start_day = (now + datetime.timedelta(days=-4)).strftime("%Y%m%d")
        end_day = akshare_today
        for stock_code in stock_codes:
            print('handle %s' % stock_code)
            try:
                stock_reviews = StockReview.objects.filter(code=stock_code).order_by('-id')[:5]
                total_volumes = 0
                for st_review in stock_reviews:
                    total_volumes += st_review.volume
                ma5 = total_volumes / 5

                recent_3_stock_reviews = stock_reviews[:3]

                latest_st_review = stock_reviews[0]
                latest_st_review.createdAt = zero_today

                if recent_3_stock_reviews[0].volume > recent_3_stock_reviews[1].volume > \
                        recent_3_stock_reviews[2].volume:
                    latest_st_review.smallVolumeUp = 1

                if latest_st_review.volume >= ma5:
                    latest_st_review.volumeBreakUpMa5 = 1

                i = 1
                for st_review in stock_reviews:
                    if st_review.smallUp == 0:
                        break
                    if i == 2:
                        st_review.last2Up = 1
                    if i == 3:
                        st_review.last3Up = 1
                    if i == 5:
                        st_review.last5Up = 1
                all_st_reviews.append(latest_st_review)

            except:
                print(stock_code)
                pass

        if len(all_st_reviews) > 0:
            bulk_update(all_st_reviews, update_fields=['smallVolumeUp', 'volumeBreakUpMa5', 'last2Up', 'last3Up', 'last5Up', 'createdAt'])  # updates only name column
