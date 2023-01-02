import datetime

import easyquotation
import akshare as ak
from django.core.management.base import BaseCommand

from stock.models import Stock, StockReview


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        stock_reviews = StockReview.objects.filter(upLimitType=1)
        stock_review_codes = [sr.code for sr in stock_reviews]

        stock_em_zt_pool_df = ak.stock_zt_pool_em(date='20221230')
        stock_codes = [st[1] for st in stock_em_zt_pool_df.values]
        print(set(stock_codes) - set(stock_review_codes))