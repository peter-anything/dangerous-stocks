import datetime

from django.core.management.base import BaseCommand

from stock.models import StockReviewRecent60, StockStatistics


class Command(BaseCommand):
    help = 'test'

    def cal_statistics(self, block_st_reviews):
        latest_st_review = block_st_reviews[0]

        total_60_volume = 0
        total_20_volume = 0
        total_10_volume = 0
        total_5_volume = 0

        total_60_price = 0
        total_20_price = 0
        total_10_price = 0
        total_5_price = 0

        idx = 1
        for block_review in block_st_reviews:
            if idx <= 5:
                total_5_volume += block_review.volume
                total_10_volume += block_review.volume
                total_20_volume += block_review.volume
                total_60_volume += block_review.volume

                total_5_price += block_review.now
                total_10_price += block_review.now
                total_20_price += block_review.now
                total_60_price += block_review.now
            elif idx <= 10:
                total_10_volume += block_review.volume
                total_20_volume += block_review.volume
                total_60_volume += block_review.volume

                total_10_price += block_review.now
                total_20_price += block_review.now
                total_60_price += block_review.now
            elif idx <= 20:
                total_20_volume += block_review.volume
                total_60_volume += block_review.volume

                total_20_price += block_review.now
                total_60_price += block_review.now
            elif idx <= 60:
                total_60_volume += block_review.volume

                total_60_price += block_review.now

            idx += 1

        priceMA60 = total_60_price / len(block_st_reviews)
        priceMA20 = total_20_price / 20
        priceMA10 = total_10_price / 10
        priceMA5 = total_5_price / 5

        volMA60 = total_60_volume / len(block_st_reviews)
        volMA20 = total_20_volume / 20
        volMA10 = total_10_volume / 10
        volMA5 = total_5_volume / 5

        return StockStatistics(
            code=latest_st_review.code,
            priceMA5=priceMA5,
            priceMA10=priceMA10,
            priceMA20=priceMA20,
            priceMA60=priceMA60,
            volMA5=volMA5,
            volMA10=volMA10,
            volMA20=volMA20,
            volMA60=volMA60
        )

    def handle(self, *args, **options):
        now = datetime.datetime.now()

        stock_reviews = StockReviewRecent60.objects \
            .order_by('code', '-id') \
            .exclude(code__istartswith='30') \
            .exclude(code__istartswith='688') \
            .exclude(name__startswith='*ST') \
            .exclude(marketValue__lt=40) \
            .all()

        pre_st_review = None

        block_st_reviews = []
        stock_statistics_arr = []
        for stock_review in stock_reviews:
            if pre_st_review:
                if stock_review.code == pre_st_review.code:
                    block_st_reviews.append(stock_review)
                else:
                    stock_statistics = self.cal_statistics(block_st_reviews)
                    stock_statistics_arr.append(stock_statistics)
                    block_st_reviews = [stock_review]
            else:
                block_st_reviews.append(stock_review)

            pre_st_review = stock_review

        StockStatistics.objects.bulk_create(stock_statistics_arr)
