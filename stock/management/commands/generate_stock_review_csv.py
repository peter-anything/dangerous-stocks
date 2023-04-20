import csv
import datetime
import json
import os

from django.core.management.base import BaseCommand

from stock.models import StockReview


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

        before_x_day = zero_today + datetime.timedelta(days=-6)

        open_time = zero_today + datetime.timedelta(hours=9, minutes=30)

        mid_open_time = zero_today + datetime.timedelta(hours=13, minutes=0)

        # 午盘
        mid_day = zero_today + datetime.timedelta(hours=12, minutes=59)

        late_day = zero_today + datetime.timedelta(hours=15)

        curr_day = late_day
        if now < mid_day:
            curr_day = mid_day

        stock_reviews = StockReview.objects.filter(createdAt__gt=zero_today) \
            .order_by('code', '-id') \
            .exclude(code__istartswith='30') \
            .exclude(code__istartswith='688') \
            .exclude(name__startswith='*ST') \
            .exclude(marketValue__lt=40) \
            .all()
        stock_statistics = {
            'bigUp': [],  # 5
            'smallUp': [],  # 2.9-5
            'up': [],  # 1.9 - 2.9
            'upDown': [],  # -1.9 ~ 1.9
            'down': [],  # -3 ~ -2
            'smallDown': [],  # -5 ~ -3,
            'bigDown': [],  # -5,
        }

        industry_item_map = {}
        hot_concepts = {}
        for candi_stock in stock_reviews:
            if candi_stock.growthRate >= 4:
                stock_statistics['bigUp'].append(candi_stock)
                if candi_stock.concepts:
                    for concept in json.loads(candi_stock.concepts):
                        hot_concepts[concept] = hot_concepts.get(concept, 0) + 1
            elif candi_stock.growthRate >= 2.9:
                stock_statistics['smallUp'].append(candi_stock)
                for concept in json.loads(candi_stock.concepts):
                    hot_concepts[concept] = hot_concepts.get(concept, 0) + 1
            elif candi_stock.growthRate >= 1.9:
                stock_statistics['up'].append(candi_stock)
            elif candi_stock.growthRate >= -1.9:
                stock_statistics['upDown'].append(candi_stock)
            elif candi_stock.growthRate >= -2.9:
                stock_statistics['down'].append(candi_stock)
            elif candi_stock.growthRate >= -4:
                stock_statistics['smallDown'].append(candi_stock)
            else:
                stock_statistics['bigDown'].append(candi_stock)

            if candi_stock.growthRate < 2:
                continue
            industry_item = industry_item_map.get(candi_stock.industry, IndustryItem(candi_stock.industry, []))
            industry_item.stocks.append(candi_stock)
            industry_item_map[candi_stock.industry] = industry_item

        concepts = sorted(hot_concepts.items(), key=lambda x: x[1], reverse=True)
        for concept in concepts:
            if concept[1] < 10:
                continue
            print(concept)

        industry_items = list(industry_item_map.values())


        industry_items = sorted(industry_items, key=lambda x: len(x.stocks), reverse=True)

        today_str = zero_today.strftime("%Y-%m-%d")

        daily_selected_stock_dir = '/Users/wangxiaobin/Documents/行情/每日精选/'

        today_dir = os.path.join(daily_selected_stock_dir, today_str)

        if not os.path.exists(today_dir):
            os.makedirs(today_dir)

        with open(os.path.join(today_dir, '每日复盘整理1.csv'), 'w') as f:
            fw = csv.writer(f)
            fw.writerow(['股票代码', '股票名称', '股票市值', '股票行业', '股票概念', '涨幅'])
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
                        [str(st.code) + '_code', st.name, st.marketValue, st.industry, st.concepts, st.growthRate])
                fw.writerow([])

        up_map = {
            'bigUp': '大阳',  # 5
            'smallUp': '小阳',  # 2.9-5
            'up': '上涨',  # 1.9 - 2.9
            'upDown': '振荡',  # -1.9 ~ 1.9
            'down': '下跌',  # -3 ~ -2
            'smallDown': '小跌',  # -5 ~ -3,
            'bigDown': '大跌',  # -5,
        }

        hot_concepts = set()
        for up_key, up_val in up_map.items():

            file_name = os.path.join(today_dir, '{}复盘整理2.csv'.format(up_val))
            with open(file_name, 'w') as f:
                    fw = csv.writer(f)
                    fw.writerow(['股票代码', '股票名称', '股票市值', '股票行业', '股票概念', '涨幅'])
                    first_count_eq_1 = False

                    big_up_stocks = stock_statistics[up_key]

                    industry_item_map = {}
                    for st in big_up_stocks:
                        industry_item = industry_item_map.get(st.industry, IndustryItem(st.industry, []))
                        industry_item.stocks.append(st)
                        industry_item_map[st.industry] = industry_item

                    industry_items = list(industry_item_map.values())
                    industry_items = sorted(industry_items, key=lambda x: len(x.stocks), reverse=True)
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
                                [str(st.code) + '_code', st.name, st.marketValue, st.industry, st.concepts, st.growthRate])
                        fw.writerow([])
