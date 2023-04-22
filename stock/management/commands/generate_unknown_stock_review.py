import datetime

import tushare as ts
from django.core.management.base import BaseCommand

from stock.models import Stock, StockReview, StockReviewRecent60


def get_stock_type(stock_code):
    """判断股票ID对应的证券市场
    匹配规则
    ['50', '51', '60', '90', '110'] 为 sh
    ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    ['5', '6', '9'] 开头的为 sh， 其余为 sz
    :param stock_code:股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
    :return 'sh' or 'sz'"""
    assert type(stock_code) is str, "stock code need str type"
    sh_head = ("50", "51", "60", "90", "110", "113", "118",
               "132", "204", "5", "6", "9", "7")
    if stock_code.startswith(("sh", "sz", "zz")):
        return stock_code[:2]
    else:
        return "SH" if stock_code.startswith(sh_head) else "SZ"


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        all_stocks = Stock.objects \
            .exclude(code__istartswith='300').exclude(code__istartswith='688').exclude(name__startswith='ST') \
            .exclude(name__startswith='*ST') \
            .filter(market='A股')

        now = datetime.datetime.now()

        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond)

        # 午盘
        mid_day = zero_today + datetime.timedelta(hours=12, minutes=59)

        late_day = zero_today + datetime.timedelta(hours=15)

        curr_day = late_day
        if now < mid_day:
            curr_day = mid_day

        # 初始化pro接口
        pro = ts.pro_api('1c4de25fce18d01933816f3b59c538f55ed362d5ddd23b8c6d4028bf')

        stock_codes = [stock_fundamental.code for stock_fundamental in all_stocks]
        stocks = Stock.objects.filter(code__in=[str(stock_code) for stock_code in stock_codes])
        stock_map = {}
        for stock in stocks:
            stock_map[stock.code] = stock
        # real_result = quotation.real([str(stock_code) for stock_code in stock_codes])
        now = datetime.datetime.now()
        stock_review_arr = []

        st_code_list = []
        for st in stocks:
            st_code_list.append('%s.%s' % (st.code, get_stock_type(st.code)))

        df_all = pro.daily(ts_code='000003.SH', start_date='20230328',
                           end_date='20230328')
        df_map = {}
        page_count = (len(st_code_list) - 1) / 100 + 1
        for i in range(int(page_count)):

            p_st_code_list = st_code_list[100 * i:100 * (i + 1)]
            # 拉取数据
            df_all = pro.daily(ts_code=','.join(p_st_code_list), start_date='20230328',
                               end_date='20230328')

            for i in range(len(df_all.values)):
                df = df_all.iloc[i]
                df_map[df['ts_code'][:6]] = df

        curr_day = datetime.datetime(2023, 3, 28, 15, 0, 0)

        for st in stocks:
            if st.code not in df_map:
                print(st.code)
                continue

            df_columns = df_map[st.code]
            # code = df_columns['ts_code']
            # name = df_columns['name']
            now = df_columns['close']
            open = df_columns['open']
            close = df_columns['close']
            high = df_columns['high']
            low = df_columns['low']
            pre_close = df_columns['pre_close']
            # bid_price = df_columns['bid1']
            #    upLimitType = models.IntegerField() # 1、 涨停 2、 跌停 3、上涨 4、下跌 5、平
            if open > 0 and close > 0:
                grow_rate = df_columns['pct_chg']

                stock_review = StockReviewRecent60()
                stock_review.code = st.code
                stock_review.name = st.name
                stock_review.open = open
                stock_review.close = df_columns['pre_close']
                stock_review.high = high
                stock_review.low = low
                stock_review.now = close
                stock_review.createdAt = curr_day
                # stock_review.marketValue = detail['总市值']
                stock_review.volume = df_columns['vol'] * 100
                # stock_review.tradingMarketValue = detail['流通市值']
                # stock_review.turnoverRate = detail['turnover']
                # stock_review.pe = detail['PE']
                stock_review.upLimit = pre_close * (1 + 0.1)
                stock_review.downLimit = pre_close * (1 - 0.1)

                if 3 >= grow_rate >= 1:
                    stock_review.smallUp = 1

                stock_review.everUpLimited = 0

                if -0.000001 <= stock_review.upLimit - stock_review.now <= 0.000001:
                    stock_review.upLimitType = 1
                else:
                    if -0.000001 <= stock_review.downLimit - stock_review.now <= 0.000001:
                        stock_review.upLimitType = 2
                    elif grow_rate > 0:
                        stock_review.upLimitType = 3
                    elif grow_rate < 0:
                        stock_review.upLimitType = 4
                    elif grow_rate == 0:
                        stock_review.upLimitType = 5

                    if -0.000001 <= stock_review.upLimit - stock_review.high <= 0.000001:
                        stock_review.everUpLimited = 1

                stock_review.industry = stock_map[st.code].industry
                stock_review.concepts = stock_map[st.code].concepts
                stock_review.type = stock_map[st.code].type
                stock_review.growthRate = grow_rate
                # stock_review.bid1Money = detail['bid1'] * detail['bid1_volume'] / 10000000
                stock_review_arr.append(stock_review)

        StockReviewRecent60.objects.bulk_create(stock_review_arr)
