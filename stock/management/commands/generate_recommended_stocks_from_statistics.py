import csv
import datetime
import os

from django.core.management.base import BaseCommand

from stock.models import Stock, StockReview, StockStatistics


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

        stock_statistics = StockStatistics.objects\
            .filter(profitLossRatio__gte=1, profitRate__lt=20)\
            .order_by('-profitRate')
        codes = [s.code for s in stock_statistics]
        x_day = datetime.datetime(2023, 4, 21, 14, 0, 0)

        ss_map = {}
        for ss in stock_statistics:
            ss_map[ss.code] = ss

        stock_reviews = StockReview.objects.filter(createdAt__gt=x_day).filter(code__in=codes) \
                .order_by('code', '-createdAt').exclude(name__startswith='*ST').all()
        industry_item_map = {}
        for candi_stock in stock_reviews:
            industry_item = industry_item_map.get(candi_stock.industry, IndustryItem(candi_stock.industry, []))
            industry_item.stocks.append(candi_stock)
            industry_item_map[candi_stock.industry] = industry_item
        industry_items = list(industry_item_map.values())

        industry_items = sorted(industry_items, key=lambda x: len(x.stocks), reverse=True)

        daily_selected_stock_dir = '/Users/wangxiaobin/Documents/行情/每日精选/'

        today_str = zero_today.strftime("%Y-%m-%d")

        today_dir = os.path.join(daily_selected_stock_dir, today_str)

        if not os.path.exists(today_dir):
            os.makedirs(today_dir)

        with open(os.path.join(today_dir, '统计数据股票推荐.csv'), 'w') as f:
            fw = csv.writer(f)
            fw.writerow(['股票代码', '股票名称', '股票市值', '股票行业', '股票概念', '涨幅', '盈亏比', '盈利', '亏损'])
            first_count_eq_1 = False
            for industry_item in industry_items:
                stocks = industry_item.stocks

                # if len(stocks) == 1 and not first_count_eq_1:
                #     fw.writerow([])
                #     fw.writerow([])
                #     fw.writerow([])
                #     fw.writerow([])
                #     fw.writerow([])
                #     first_count_eq_1 = True
                stocks = sorted(stocks, key=lambda x: x.growthRate)
                for st in stocks:
                    if st.now < ss_map[st.code].priceMA60:
                        continue

                    fw.writerow([str(st.code) + '_code', st.name,
                                 st.marketValue, st.industry,
                                 st.concepts, st.growthRate,
                                 ss_map[st.code].profitLossRatio, ss_map[st.code].profitRate,
                                 ss_map[st.code].lossRate])
