import csv
import datetime
import json
import os

import easyquotation
from django.core.management.base import BaseCommand

from stock.conf.my_import_stocks import MY_IMPORTANT_STOCKS
from stock.models import Stock, StockStatistics, StockReview, RecommendStockInRealTime
from stock.util.stock_util import get_stock_statistics_map, gen_stock_review


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
        open_time = zero_today + datetime.timedelta(hours=9, minutes=30)

        mid_open_time = zero_today + datetime.timedelta(hours=13, minutes=0)

        # 午盘
        mid_day = zero_today + datetime.timedelta(hours=12, minutes=59)

        late_day = zero_today + datetime.timedelta(hours=15)

        # if not (open_time < now < late_day):
        #     print('未开盘或者已收盘')
        #     return

        all_stocks = Stock.objects \
            .exclude(code__istartswith='300').exclude(code__istartswith='688').exclude(name__startswith='ST') \
            .exclude(name__startswith='*ST') \
            .filter(market='A股')

        stock_map = {}
        for stock in all_stocks:
            stock_map[stock.code] = stock

        st_name_map = {}
        for st in all_stocks:
            st_name_map[st.name] = st.code

        my_import_codes = []
        quotation = easyquotation.use('tencent')

        stock_statistics_map = get_stock_statistics_map(zero_today + datetime.timedelta(days=-1),
                                                        zero_today + datetime.timedelta(days=-1, hours=16))
        candi_stocks = []

        industry_item_map = {}
        idx = 1
        for industry, industry_detail in MY_IMPORTANT_STOCKS.items():
            industry_codes = [st_name_map[name] for name in industry_detail['names']]
            real_result = quotation.real([str(stock_code) for stock_code in industry_codes])

            industry_monitor_stocks = []
            for stock_code, detail in real_result.items():
                stock_review = gen_stock_review(detail, stock_map, zero_today)

                if not stock_review:
                    continue
                stock_review.turnover = detail['成交额(万)']

                max_up_limit = (detail['now'] - detail['low']) * 100 / detail['low']
                if not max_up_limit >= industry_detail['upLimit']:
                    continue
                    #
                    # if now > priceMA5:
                    #     print('股票：%s, 股价大于5日线' % name)
                    # elif now > priceMA10:
                    #     print('股票：%s, 股价大于10日线' % name)
                    # elif now > priceMA20:
                    #     print('股票：%s, 股价大于20日线' % name)
                    # elif now > priceMA60:
                    #     print('股票：%s, 股价大于60日线' % name)
                    # else:
                    #     print('股票：%s, 股价大于60日线' % name)

                industry_item = industry_item_map.get(stock_review.industry, IndustryItem(stock_review.industry, []))
                industry_item.stocks.append(stock_review)
                industry_item_map[stock_review.industry] = industry_item
                candi_stocks.append(stock_review)

            if len(industry_monitor_stocks) >= ((len(industry_codes) - 1) / 2 + 1) or len(industry_monitor_stocks) >= 3:
                print('%s 有行情, 包含股票: [%s]' % (industry, [st['name'] for st in industry_monitor_stocks]))
        industry_items = list(industry_item_map.values())

        industry_items = sorted(industry_items, key=lambda x: len(x.stocks), reverse=True)

        daily_selected_stock_dir = '/Users/wangxiaobin/Documents/行情/每日精选/'

        today_str = zero_today.strftime("%Y-%m-%d")

        today_dir = os.path.join(daily_selected_stock_dir, today_str, '实时监控')

        if not os.path.exists(today_dir):
            os.makedirs(today_dir)

        now = datetime.datetime.now()

        w_path = os.path.join(today_dir, '重点观察所有股票-{}.csv'.format(now.strftime('%H时%M分%S秒')))

        rs_arr = []
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
                    ss = stock_statistics_map[st.code]
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
                    openHighRate = (100 * (st.open - st.close) / st.close)
                    nowRate = (100 * (st.now - st.close) / st.close)
                    bottomUpRate = (100 * (st.now - st.low) / st.low)

                    rs = RecommendStockInRealTime(code=st.code,
                                                  name=st.name,
                                                  industry=st.industry,
                                                  marketValue=st.marketValue,
                                                  turnoverRate=st.turnoverRate,
                                                  openHighRate=openHighRate,
                                                  bottomUpRate=bottomUpRate,
                                                  nowRate=nowRate,
                                                  turnover=st.turnover / 100000000,
                                                  recent5ProfitLossRatio='盈利：%s/亏损：%s' % (
                                                      round(recent_5_profit_ratio, 2), round(recent_5_loss_ratio, 2)),
                                                  recent10ProfitLossRatio='盈利：%s/亏损：%s' % (
                                                      round(recent_10_profit_ratio, 2), round(recent_10_loss_ratio, 2)),
                                                  recent20ProfitLossRatio='盈利：%s/亏损：%s' % (
                                                      round(recent_20_profit_ratio, 2), round(recent_20_loss_ratio, 2)),
                                                  )
                    rs_arr.append(rs)

                    if recent_5_profit_ratio > recent_5_loss_ratio:
                        rs.canBuy = 1
                    csv_rows = [str(st.code) + '_code', st.name,
                                st.marketValue, st.industry,
                                st.concepts, st.growthRate,
                                '盈利：%s/亏损：%s' % (round(recent_5_profit_ratio, 2), round(recent_5_loss_ratio, 2)),
                                '盈利：%s/亏损：%s' % (round(recent_10_profit_ratio, 2), round(recent_10_loss_ratio, 2)),
                                '盈利：%s/亏损：%s' % (round(recent_20_profit_ratio, 2), round(recent_20_loss_ratio, 2))]
                    fw.writerow(csv_rows)
                    print(csv_rows)

                fw.writerow([])

        if len(rs_arr) > 0:
            RecommendStockInRealTime.objects.bulk_create(rs_arr)