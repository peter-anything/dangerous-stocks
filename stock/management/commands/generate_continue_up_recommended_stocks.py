import csv
import datetime
import os

from django.core.management.base import BaseCommand

from stock.models import StockReview
import matplotlib.pyplot as plt



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

        before_x_day = zero_today + datetime.timedelta(days=-21)

        open_time = zero_today + datetime.timedelta(hours=9, minutes=30)

        mid_open_time = zero_today + datetime.timedelta(hours=13, minutes=0)

        # 午盘
        mid_day = zero_today + datetime.timedelta(hours=12, minutes=59)

        late_day = zero_today + datetime.timedelta(hours=15)

        curr_day = late_day
        if now < mid_day:
            curr_day = mid_day

        stock_reviews = StockReview.objects.filter(createdAt__gt=before_x_day) \
            .order_by('code', '-id') \
            .exclude(code__istartswith='30') \
            .exclude(code__istartswith='688') \
            .exclude(name__startswith='*ST') \
            .exclude(marketValue__lt=40) \
            .all()

        pre_st_review = None

        block_st_reviews = []
        candi_stocks = []
        for stock_review in stock_reviews:
            if pre_st_review:
                if stock_review.code == pre_st_review.code:
                    block_st_reviews.append(stock_review)
                else:
                    block_st_reviews = [stock_review]
            else:
                block_st_reviews.append(stock_review)

            pre_st_review = stock_review

            if len(block_st_reviews) == 15:
                lowest_price_arr = []
                highest_price_arr = []
                close_price_arr = []
                for st in block_st_reviews:
                    lowest_price_arr.append(st.low)
                    highest_price_arr.append(st.high)
                    close_price_arr.append(st.close)

                avg_low_price = sum(lowest_price_arr) / 15
                avg_high_price = sum(highest_price_arr) / 15
                close_price_arr = sum(close_price_arr) / 15
                latest_stock = block_st_reviews[0]

                if -0.002 < (latest_stock.close - avg_low_price) / avg_low_price < 0.002:
                    if latest_stock.growthRate > 1:
                        candi_stocks.append(stock_review)

        industry_item_map = {}
        for candi_stock in candi_stocks:
            industry_item = industry_item_map.get(candi_stock.industry, IndustryItem(candi_stock.industry, []))
            industry_item.stocks.append(candi_stock)
            industry_item_map[candi_stock.industry] = industry_item
        industry_items = list(industry_item_map.values())

        with open('continue_up_stocks.csv', 'w', newline='\n') as f:
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
