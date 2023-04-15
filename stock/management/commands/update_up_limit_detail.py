from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

import akshare as ak

from stock.models import StockReview


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        akshare_today = now.strftime("%Y%m%d")

        zero_today = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond)

        # 午盘
        mid_day = zero_today + timedelta(hours=12, minutes=59)

        late_day = zero_today + timedelta(hours=15)

        createdAt = datetime.now().strftime("%Y-%m-%d")

        start_t = createdAt + ' 00:00:00'
        end_t = createdAt + ' 23:59:59'
        if now < mid_day:
            end_t = createdAt + ' 13:00:00'
            curr_day = mid_day
        if now > late_day:
            start_t = createdAt + ' 13:00:01'
            curr_day = late_day

        stock_em_zt_pool_df = ak.stock_zt_pool_em(date=akshare_today)
        for stock in stock_em_zt_pool_df.values:
            id, code, name, growth_rate, now_price, tradingV, tradingMarketValue, marketValue, turnoverRate, closeMony, firstUpLimitTime, finalUpLimitTime, breakUpLimitCount, UpLimitStatistics, continuousUpLimitCount, industry = stock
            StockReview.objects.filter(code=code, createdAt__lt=end_t, createdAt__gt=start_t).update(
                firstUpLimitTime='%s %s:%s:%s' % (today, firstUpLimitTime[0:2], firstUpLimitTime[2:4], firstUpLimitTime[4:6]),
                finalUpLimitTime='%s %s:%s:%s' % (today, finalUpLimitTime[0:2], finalUpLimitTime[2:4], finalUpLimitTime[4:6]),
                breakUpLimitCount=breakUpLimitCount,
                continuousUpLimitCount=continuousUpLimitCount,
                upDownStatistics=UpLimitStatistics,
                createdAt=curr_day
            )