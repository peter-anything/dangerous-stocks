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
        stock_codes = [stock.code for stock in all_stocks]

        all_st_reviews = []
        for stock_code in stock_codes:
            print('handle %s' % stock_code)
            try:
                stock_reviews = StockReview.objects.filter(code=stock_code).order_by('-id')[:5]
                for st_review in stock_reviews:
                    if 3 >= st_review.growthRate >= 1:
                        st_review.smallUp = 1
                    all_st_reviews.append(st_review)
            except:
                pass

        if len(all_st_reviews) > 0:
            bulk_update(all_st_reviews, update_fields=['smallUp'])  # updates only name column
