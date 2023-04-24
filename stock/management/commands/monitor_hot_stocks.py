from django.core.management.base import BaseCommand

from stock.models import Stock, StockStatistics, StockReviewRecent60


class IndustryItem(object):
    industry = ''
    stocks = []

    def __init__(self, industry, stocks):
        self.industry = industry
        self.stocks = stocks


class AdditionalNum(object):
    value = 0.0
    idx = 0
    is_inflection = False

    def __init__(self, value, idx):
        self.value = value
        self.idx = idx


class Command(BaseCommand):
    help = 'test'

    def cal_statistics_recent_x_days(self, block_st_reviews, recent_x_days):
        if len(block_st_reviews) < 3:
            return None
        high_prices = []
        low_prices = []
        now_prices = []
        volumes = []
        for st in block_st_reviews:
            high_prices.append(st.high)
            low_prices.append(st.low)
            now_prices.append(st.now)
            volumes.append(st.volume)

        for recent_x_day in recent_x_days:
            if block_st_reviews[0].code == '000610':
                print('test')
            days = recent_x_day['days']
            upRate = recent_x_day['upRate']
            curr_upRate = 0
            low_curr_idx = 0
            high_curr_idx = 0
            # sorted_now_prices = sorted(now_prices, reverse=True)
            selected_prices = now_prices[:days]
            additional_nums = []
            for i, p in enumerate(selected_prices):
                additional_nums.append(AdditionalNum(p, i))

            sorted_additional_nums = sorted(additional_nums, key=lambda x: x.value, reverse=True)
            for sorted_additional_num in sorted_additional_nums:
                selected_idx = sorted_additional_num.idx
                if selected_idx == len(selected_prices) - 1 or selected_idx == 0:
                    sorted_additional_num.is_inflection = False
                    continue

                if selected_prices[selected_idx + 1] > sorted_additional_num.value \
                        and selected_prices[selected_idx - 1] > sorted_additional_num.value:
                    right_up_rate = (selected_prices[selected_idx + 1] - sorted_additional_num.value) / sorted_additional_num.value
                    left_up_rate = (selected_prices[selected_idx + 1] - sorted_additional_num.value) / sorted_additional_num.value
                    if right_up_rate * 100 >= 1:
                        sorted_additional_num.is_inflection = True
                        continue

                    if left_up_rate * 100 >= 1:
                        sorted_additional_num.is_inflection = True
                        continue
                    sorted_additional_num.is_inflection = False

            for num in additional_nums:
                if num.is_inflection:
                    print('最近天数：{}, 最好起涨点：{}, 代码: {}'.format(days, num.idx, block_st_reviews[0].code))
                    return

            #
            # while curr_upRate < upRate:
            #
            #     while now_prices[low_curr_idx] >= now_prices[low_curr_idx + 1] and low_curr_idx < days - 1:
            #         low_curr_idx += 1
            #
            #     while now_prices[high_curr_idx] < now_prices[high_curr_idx + 1] and high_curr_idx < days - 1:
            #         high_curr_idx += 1
            #
            #     curr_low = now_prices[low_curr_idx]
            #     curr_high = now_prices[high_curr_idx]
            #
            #     if high_curr_idx > low_curr_idx:
            #         low_curr_idx = high_curr_idx
            #         continue
            #
            #     curr_upRate = (curr_high - curr_low) * 100 / curr_low
            #
            #     if curr_upRate < upRate:
            #         low_curr_idx = high_curr_idx - 1

    def handle(self, *args, **options):
        all_stocks = Stock.objects \
            .exclude(code__istartswith='300').exclude(code__istartswith='688').exclude(name__startswith='ST') \
            .exclude(name__startswith='*ST') \
            .filter(market='A股')
        stock_map = {}
        for stock in all_stocks:
            stock_map[stock.code] = stock

        top3_stock_statistics = StockStatistics.objects.order_by('-last3UpRate')[:30]

        top3_stock_pool = {}
        top5_stock_pool = {}
        top20_stock_pool = {}
        hot_codes = set()
        for ss in top3_stock_statistics:
            st = stock_map[ss.code]
            hot_codes.add(ss.code)
            top3_stock_pool[st.code] = ss

        top5_stock_statistics = StockStatistics.objects.order_by('-last5UpRate')[:30]
        for ss in top5_stock_statistics:
            st = stock_map[ss.code]
            hot_codes.add(ss.code)
            top5_stock_pool[st.code] = ss

        top20_stock_statistics = StockStatistics.objects.order_by('-last20UpRate')[:30]
        for ss in top20_stock_statistics:
            st = stock_map[ss.code]
            hot_codes.add(ss.code)
            top20_stock_pool[st.code] = ss

        st_reviews = StockReviewRecent60.objects \
            .filter(code__in=hot_codes) \
            .order_by('code', '-createdAt').all()

        pre_st_review = None
        block_st_reviews = []
        stock_statistics_arr = []
        for stock_review in st_reviews:
            if pre_st_review:
                if stock_review.code == pre_st_review.code:
                    block_st_reviews.append(stock_review)
                else:
                    recent_x_days = []
                    if block_st_reviews[0].code in top3_stock_pool:
                        recent_x_days.append({
                            'days': 3,
                            'upRate': top3_stock_pool[block_st_reviews[0].code].last3UpRate
                        })
                    elif block_st_reviews[0].code in top5_stock_pool:
                        recent_x_days.append({
                            'days': 5,
                            'upRate': top5_stock_pool[block_st_reviews[0].code].last5UpRate
                        })
                    elif block_st_reviews[0].code in top20_stock_pool:
                        recent_x_days.append({
                            'days': 20,
                            'upRate': top20_stock_pool[block_st_reviews[0].code].last20UpRate
                        })

                    self.cal_statistics_recent_x_days(block_st_reviews, recent_x_days)
                    # if stock_statistics:
                    #     stock_statistics_arr.append(stock_statistics)
                    block_st_reviews = [stock_review]
            else:
                block_st_reviews.append(stock_review)

            pre_st_review = stock_review
