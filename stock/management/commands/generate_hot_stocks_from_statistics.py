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
        x_day = zero_today

        hot_codes = set()
        hot_3_stock_statistics = StockStatistics.objects\
            .order_by('-last3UpRate')[:30]
        for s in hot_3_stock_statistics:
            hot_codes.add(s.code)
        hot_5_stock_statistics = StockStatistics.objects \
            .order_by('-last5UpRate')[:30]
        for s in hot_5_stock_statistics:
            hot_codes.add(s.code)
        hot_10_stock_statistics = StockStatistics.objects \
            .order_by('-last10UpRate')[:30]
        for s in hot_10_stock_statistics:
            hot_codes.add(s.code)
        hot_20_stock_statistics = StockStatistics.objects \
            .order_by('-last20UpRate')[:200]
        for s in hot_20_stock_statistics:
            hot_codes.add(s.code)

        stock_reviews = StockReview.objects.filter(createdAt__gt=x_day).filter(code__in=hot_codes) \
                .order_by('code', '-createdAt').exclude(name__startswith='*ST').all()

        st_map = {}
        for sr in stock_reviews:
            st_map[sr.code] = sr

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

        with open(os.path.join(today_dir, '最近三天大涨股票.csv'), 'w') as f:
            fw = csv.writer(f)
            fw.writerow(['股票代码', '股票名称', '股票市值', '股票行业', '股票概念', '涨幅', '最近涨幅', '盈亏比', '盈利', '亏损'])
            for s in hot_3_stock_statistics:
                if s.code not in st_map:
                    continue
                st = st_map[s.code]
                fw.writerow([str(st.code) + '_code', st.name,
                             st.marketValue, st.industry,
                             st.concepts, st.growthRate,
                             s.last3UpRate, s.profitLossRatio,
                             s.profitRate, s.lossRate])

        with open(os.path.join(today_dir, '最近五天大涨股票.csv'), 'w') as f:
            fw = csv.writer(f)
            fw.writerow(['股票代码', '股票名称', '股票市值', '股票行业', '股票概念', '涨幅', '最近涨幅', '盈亏比', '盈利', '亏损'])
            for s in hot_5_stock_statistics:
                st = st_map[s.code]
                fw.writerow([str(st.code) + '_code', st.name,
                             st.marketValue, st.industry,
                             st.concepts, st.growthRate,
                             s.last5UpRate, s.profitLossRatio,
                             s.profitRate, s.lossRate])

        with open(os.path.join(today_dir, '最近十天大涨股票.csv'), 'w') as f:
            fw = csv.writer(f)
            fw.writerow(['股票代码', '股票名称', '股票市值', '股票行业', '股票概念', '涨幅', '最近涨幅', '盈亏比', '盈利', '亏损'])
            for s in hot_10_stock_statistics:
                st = st_map[s.code]
                fw.writerow([str(st.code) + '_code', st.name,
                             st.marketValue, st.industry,
                             st.concepts, st.growthRate,
                             s.last10UpRate, s.profitLossRatio,
                             s.profitRate, s.lossRate])

        with open(os.path.join(today_dir, '最近二十天大涨股票.csv'), 'w') as f:
            fw = csv.writer(f)
            fw.writerow(['股票代码', '股票名称', '股票市值', '股票行业', '股票概念', '涨幅', '最近涨幅', '盈亏比', '盈利', '亏损'])
            for s in hot_20_stock_statistics:
                st = st_map[s.code]
                fw.writerow([str(st.code) + '_code', st.name,
                             st.marketValue, st.industry,
                             st.concepts, st.growthRate,
                             s.last20UpRate, s.profitLossRatio,
                             s.profitRate, s.lossRate])