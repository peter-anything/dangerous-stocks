import csv
import datetime
import json
import os

from django.core.management.base import BaseCommand

from stock.conf.my_import_stocks import MY_IMPORTANT_STOCKS
from stock.models import HourStockReview, Stock
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
        now = datetime.datetime.now()

        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond)

        all_stocks = Stock.objects \
            .exclude(code__istartswith='300').exclude(code__istartswith='688').exclude(name__startswith='ST') \
            .exclude(name__startswith='*ST') \
            .filter(market='A股')

        st_name_map = {}
        for st in all_stocks:
            st_name_map[st.name] = st.code

        ss_map = get_stock_statistics_map(zero_today, zero_today + datetime.timedelta(hours=16))

        stock_codes = []
        for industry, industry_detail in MY_IMPORTANT_STOCKS.items():
            industry_codes = [st_name_map[name] for name in industry_detail['names']]
            stock_codes.extend(industry_codes)

        stock_reviews = HourStockReview.objects.filter(createdAt__gt=zero_today) \
            .order_by('code', '-id') \
            .exclude(code__istartswith='30') \
            .exclude(code__istartswith='688') \
            .exclude(name__startswith='*ST') \
            .exclude(marketValue__lt=40) \
            .filter(code__in=stock_codes) \
            .all()

        industry_item_map = {}
        for candi_stock in stock_reviews:
            if (candi_stock.now - candi_stock.open) / candi_stock.open < 0.025:
                continue
            industry_item = industry_item_map.get(candi_stock.industry, IndustryItem(candi_stock.industry, []))
            industry_item.stocks.append(candi_stock)
            industry_item_map[candi_stock.industry] = industry_item
        industry_items = list(industry_item_map.values())

        industry_items = sorted(industry_items, key=lambda x: len(x.stocks), reverse=True)

        today_str = zero_today.strftime("%Y-%m-%d")

        daily_selected_stock_dir = '/Users/wangxiaobin/Documents/行情/每日精选/'

        today_dir = os.path.join(daily_selected_stock_dir, today_str)

        if not os.path.exists(today_dir):
            os.makedirs(today_dir)

        with open(os.path.join(today_dir, '盘中突然拉升重点观察所有股票-{}.csv'.format(now.strftime('%H时%M分%S秒'))), 'w') as f:
            fw = csv.writer(f)
            fw.writerow(['股票代码', '股票名称', '股票市值', '股票行业', '股票概念', '涨幅', '五日盈亏比', '十日盈亏比', '二十日盈亏比'])
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
                    ss = ss_map[st.code]
                    recent_now_prices = json.loads(ss.recentNowPrices)
                    recent_5_now_prices = recent_now_prices[:5]
                    low_5_price = min(recent_5_now_prices)
                    high_5_price = max(recent_5_now_prices)
                    recent_10_now_prices = recent_now_prices[:10]
                    low_10_price = min(recent_10_now_prices)
                    high_10_price = max(recent_10_now_prices)
                    recent_20_now_prices = recent_now_prices[:20]
                    low_20_price = min(recent_20_now_prices)
                    high_20_price = max(recent_20_now_prices)

                    recent_5_profit_ratio = (high_5_price - st.now) * 100 / st.now
                    recent_5_loss_ratio = (st.now - low_5_price) * 100 / st.now

                    recent_10_profit_ratio = (high_10_price - st.now) * 100 / st.now
                    recent_10_loss_ratio = (st.now - low_10_price) * 100 / st.now

                    recent_20_profit_ratio = (high_20_price - st.now) * 100 / st.now
                    recent_20_loss_ratio = (st.now - low_20_price) * 100 / st.now

                    # if st.code not in ss_map:
                    #     continue
                    # if ss_map[st.code].profitLossRatio < 1:
                    #     continue
                    fw.writerow([str(st.code) + '_code', st.name,
                                 st.marketValue, st.industry,
                                 st.concepts, st.growthRate,
                                 '盈利：%s/亏损：%s' % (round(recent_5_profit_ratio, 2), round(recent_5_loss_ratio, 2)),
                                 '盈利：%s/亏损：%s' % (round(recent_10_profit_ratio, 2), round(recent_10_loss_ratio, 2)),
                                 '盈利：%s/亏损：%s' % (round(recent_20_profit_ratio, 2), round(recent_20_loss_ratio, 2))])
                fw.writerow([])
