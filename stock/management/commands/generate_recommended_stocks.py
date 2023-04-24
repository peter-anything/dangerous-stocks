import csv
import datetime
import os

from django.core.management.base import BaseCommand

from stock.models import Stock, StockReview
from stock.util.stock_util import get_stock_statistics_map


class IndustryItem(object):
    industry = ''
    stocks = []

    def __init__(self, industry, stocks):
        self.industry = industry
        self.stocks = stocks


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        all_stocks = Stock.objects \
            .exclude(code__istartswith='30').exclude(code__istartswith='688').exclude(name__startswith='ST') \
            .exclude(name__startswith='*ST') \
            .filter(market='A股')

        now = datetime.datetime.now()

        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond)

        before_6_day = zero_today + datetime.timedelta(days=-6)

        # 午盘
        mid_day = zero_today + datetime.timedelta(hours=12, minutes=59)

        late_day = zero_today + datetime.timedelta(hours=15)

        curr_day = late_day
        if now < mid_day:
            curr_day = mid_day

        stock_reviews = StockReview.objects.filter(createdAt__gt=before_6_day) \
            .order_by('code', '-createdAt') \
            .exclude(code__istartswith='30') \
            .exclude(code__istartswith='688') \
            .exclude(name__startswith='*ST')

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

            if len(block_st_reviews) == 5:
                latest_st_review = block_st_reviews[0]
                total_volume = 0
                for block_review in block_st_reviews[:]:
                    total_volume += block_review.volume

                avg_volume = total_volume / 5

                if not latest_st_review.volume >= avg_volume * 0.8:
                    continue

                is_big_up = False
                for block_review in block_st_reviews:
                    if block_review.growthRate >= 5:
                        is_big_up = True
                        break
                if is_big_up:
                    if latest_st_review.growthRate >= 2:
                        print({'name': latest_st_review.name,
                               'volume': latest_st_review.volume,
                               'concepts': latest_st_review.concepts,
                               'code': latest_st_review.code})
                        candi_stocks.append(latest_st_review)
                else:
                    if latest_st_review.growthRate >= 3:
                        print({'name': latest_st_review.name,
                               'volume': latest_st_review.volume,
                               'concepts': latest_st_review.concepts,
                               'code': latest_st_review.code})
                        candi_stocks.append(latest_st_review)

        industry_item_map = {}
        for candi_stock in candi_stocks:
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

        ss_map = get_stock_statistics_map(zero_today, zero_today + datetime.timedelta(hours=16))


        with open(os.path.join(today_dir, '收盘精选所有股票.csv'), 'w') as f:
            fw = csv.writer(f)
            fw.writerow(['股票代码', '股票名称', '股票市值', '股票行业', '股票概念', '涨幅', '盈亏比', '盈利', '亏损'])
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
                    fw.writerow([str(st.code) + '_code', st.name,
                                 st.marketValue, st.industry,
                                 st.concepts, st.growthRate,
                                 ss_map[st.code].profitLossRatio, ss_map[st.code].profitRate,
                                 ss_map[st.code].lossRate])

        with open(os.path.join(today_dir, '收盘精选推荐股票.csv'), 'w') as f:
            fw = csv.writer(f)
            fw.writerow(['股票代码', '股票名称', '股票市值', '股票行业', '股票概念', '涨幅', '盈亏比', '盈利', '亏损'])
            for industry_item in industry_items:
                stocks = industry_item.stocks

                if len(stocks) == 1:
                    continue

                stocks = sorted(stocks, key=lambda x: x.growthRate)
                for st in stocks:
                    if ss_map[st.code].profitLossRatio < 1:
                        continue
                    fw.writerow([str(st.code) + '_code', st.name,
                                 st.marketValue, st.industry,
                                 st.concepts, st.growthRate,
                                 ss_map[st.code].profitLossRatio, ss_map[st.code].profitRate,
                                 ss_map[st.code].lossRate])