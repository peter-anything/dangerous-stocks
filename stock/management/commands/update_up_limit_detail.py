import datetime

from django.core.management.base import BaseCommand

import akshare as ak

from stock.models import StockReview


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        today = '2022-12-30'
        stock_em_zt_pool_df = ak.stock_zt_pool_em(date='20221230')
        for stock in stock_em_zt_pool_df.values:
            id, code, name, growth_rate, now_price, tradingV, tradingMarketValue, marketValue, turnoverRate, closeMony, firstUpLimitTime, finalUpLimitTime, breakUpLimitCount, UpLimitStatistics, continuousUpLimitCount, industry = stock
            stock_detail = StockReview.objects.filter(code=code, createdAt__lt='%s 23:59:59' % today, createdAt__gt='%s 00:00:00' % today)
            print(stock_detail.query)
            StockReview.objects.filter(code=code, createdAt__lt='%s 23:59:59' % today, createdAt__gt='%s 00:00:00' % today).update(
                firstUpLimitTime='%s %s:%s:%s' % (today, firstUpLimitTime[0:2], firstUpLimitTime[2:4], firstUpLimitTime[4:6]),
                finalUpLimitTime='%s %s:%s:%s' % (today, finalUpLimitTime[0:2], finalUpLimitTime[2:4], finalUpLimitTime[4:6]),
                breakUpLimitCount=breakUpLimitCount,
                continuousUpLimitCount=continuousUpLimitCount,
                upDownStatistics=UpLimitStatistics,
                createdAt='%s 15:00:00' % today
            )