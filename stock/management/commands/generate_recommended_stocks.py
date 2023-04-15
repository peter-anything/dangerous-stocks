import csv
import datetime

from django.core.management.base import BaseCommand

from stock.models import Stock, StockReview


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

        stock_reviews = StockReview.objects.filter(createdAt__gt=before_6_day)\
            .order_by('code', '-id').exclude(name__startswith='*ST').all()

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
                is_big_up = False
                for block_review in block_st_reviews:
                    if block_review.growthRate >= 5:
                        is_big_up = True
                        break
                if is_big_up:
                    total_volume = 0

                    for block_review in block_st_reviews:
                        total_volume += block_review.volume

                    avg_volume = total_volume / 5

                    latest_st_review = block_st_reviews[0]
                    latest_volume = latest_st_review.volume
                    if latest_volume >= avg_volume \
                            and latest_st_review.growthRate >= 2 \
                            and latest_st_review.marketValue >= 30\
                            and not latest_st_review.code.startswith('30'):
                        print({'name': latest_st_review.name,
                               'volume': latest_st_review.volume,
                               'concepts': latest_st_review.concepts,
                               'code': latest_st_review.code})
                        candi_stocks.append(latest_st_review)

        sorted(candi_stocks, key=lambda x: x.industry)
        with open('recommend_stocks.csv', 'w') as f:
            fw = csv.writer(f)
            fw.writerow(['股票代码', '股票名称', '股票市值', '股票行业', '股票概念', '涨幅'])
            for st in candi_stocks:
                fw.writerow([str(st.code) + '_code', st.name, st.marketValue, st.industry, st.concepts, st.growthRate])

        print(len(candi_stocks))