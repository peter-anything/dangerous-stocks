import csv
import datetime
import os

from django.core.management.base import BaseCommand

from stock.models import HourStockReview


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

        stock_reviews = HourStockReview.objects.filter(createdAt__gt=zero_today) \
            .order_by('code', '-id') \
            .exclude(code__istartswith='30') \
            .exclude(code__istartswith='688') \
            .exclude(name__startswith='*ST') \
            .exclude(marketValue__lt=450)\
            .all()

        industry_item_map = {}
        for candi_stock in stock_reviews:
            open_up_rate = (candi_stock.now - candi_stock.open) * 100 / candi_stock.open
            low_up_rate = (candi_stock.now - candi_stock.low)  * 100 / candi_stock.low
            if open_up_rate >= 1 or low_up_rate >= 1:
                industry_item = industry_item_map.get(candi_stock.industry, IndustryItem(candi_stock.industry, []))
                candi_stock.open_up_rate = open_up_rate
                candi_stock.low_up_rate = low_up_rate
                industry_item.stocks.append(candi_stock)
                industry_item_map[candi_stock.industry] = industry_item
        industry_items = list(industry_item_map.values())

        industry_items = sorted(industry_items, key=lambda x: len(x.stocks), reverse=True)

        today_str = zero_today.strftime("%Y-%m-%d")

        daily_selected_stock_dir = '/Users/wangxiaobin/Documents/行情/每日精选/'

        today_dir = os.path.join(daily_selected_stock_dir, today_str)


        if not os.path.exists(today_dir):
            os.makedirs(today_dir)

        with open(os.path.join(today_dir, '盘中拉升大盘所有股票-{}.csv'.format(now.strftime('%H时%M分%S秒'))), 'w') as f:
            fw = csv.writer(f)
            fw.writerow(['股票代码', '股票名称', '股票市值', '股票行业', '股票概念', '涨幅', '开盘拉升', '低点拉升',])
            first_count_eq_1 = False
            for industry_item in industry_items:
                stocks = industry_item.stocks

                if len(stocks) == 1 and not first_count_eq_1:
                    fw.writerow([])
                    fw.writerow([])
                    fw.writerow([])
                    fw.writerow([])
                    fw.writerow([])
                    first_count_eq_1 = True
                stocks = sorted(stocks, key=lambda x: x.growthRate)
                for st in stocks:
                    fw.writerow(
                        [str(st.code) + '_code', st.name,
                         st.marketValue, st.industry,
                         st.concepts, st.growthRate,
                         st.open_up_rate, st.low_up_rate
                         ])
                fw.writerow([])