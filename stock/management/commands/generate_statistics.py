import datetime
import json

from django.core.management.base import BaseCommand

from stock.models import StockReviewRecent60, StockStatistics

now = datetime.datetime.now()

zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                      microseconds=now.microsecond)
late_day = zero_today + datetime.timedelta(hours=15)


class Command(BaseCommand):
    help = 'test'

    def cal_statistics(self, block_st_reviews):
        if len(block_st_reviews) < 3:
            return None
        latest_st_review = block_st_reviews[0]

        total_145_volume = 0
        total_60_volume = 0
        total_40_volume = 0
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
                total_40_volume += block_review.volume
                total_60_volume += block_review.volume
                total_145_volume += block_review.volume

                total_5_price += block_review.now
                total_10_price += block_review.now
                total_20_price += block_review.now
                total_60_price += block_review.now
            elif idx <= 10:
                total_10_volume += block_review.volume
                total_20_volume += block_review.volume
                total_40_volume += block_review.volume
                total_60_volume += block_review.volume
                total_145_volume += block_review.volume

                total_10_price += block_review.now
                total_20_price += block_review.now
                total_60_price += block_review.now
            elif idx <= 20:
                total_20_volume += block_review.volume
                total_40_volume += block_review.volume
                total_60_volume += block_review.volume
                total_145_volume += block_review.volume

                total_20_price += block_review.now
                total_60_price += block_review.now
            elif idx <= 40:
                total_40_volume += block_review.volume
                total_60_volume += block_review.volume
                total_145_volume += block_review.volume

                total_60_price += block_review.now
            elif idx <= 60:
                total_60_volume += block_review.volume
                total_145_volume += block_review.volume

                total_60_price += block_review.now
            elif idx <= 145:
                total_145_volume += block_review.volume

            idx += 1

        priceMA60 = total_60_price / len(block_st_reviews)
        priceMA20 = total_20_price / 20
        priceMA10 = total_10_price / 10
        priceMA5 = total_5_price / 5

        volMA145 = total_145_volume / 145
        volMA60 = total_60_volume / len(block_st_reviews)
        volMA40 = total_40_volume / 40
        volMA20 = total_20_volume / 20
        volMA10 = total_10_volume / 10
        volMA5 = total_5_volume / 5

        volCondition = 0
        priceCondition = 0
        volContinueCondition = 0

        if latest_st_review.code == '002368':
            for st in block_st_reviews[:20]:
                print(st.createdAt)
                print(st.now)

            print(latest_st_review.code)

        # 1、小于40日线，低吸 2、突破五日线, 3、连续放量
        latest_3_review = block_st_reviews[:3]
        if latest_st_review.volume < volMA40:
            volCondition = 1
        elif (latest_st_review.volume - volMA5) * 100 / volMA5 > -1 or latest_st_review.volume > volMA5:
            volCondition = 2

        # 1、连续放量
        if latest_3_review[0].volume > latest_3_review[1].volume > latest_3_review[2].volume:
            volContinueCondition = 1
        # 2、连续缩量
        elif latest_3_review[0].volume < latest_3_review[1].volume < latest_3_review[2].volume:
            volContinueCondition = 2

        # 1、远大于5日线 2、靠近五日线 3、5~10线之间 4、靠近十日线 5、 10~20日线之间 6、靠近20日线  7、20~60日线之间 8、靠近60日线 9、远离60日线
        if 1 > (latest_st_review.now - priceMA5) * 100 / priceMA5 > -1:
            priceCondition = 2
        # 4
        elif 1 > (latest_st_review.now - priceMA10) * 100 / priceMA5 > -1:
            priceCondition = 4
        # 6
        elif 1 > (latest_st_review.now - priceMA20) * 100 / priceMA5 > -1:
            priceCondition = 6
        # 8
        elif 1 > (latest_st_review.now - priceMA60) * 100 / priceMA5 > -1:
            priceCondition = 8
        elif (latest_st_review.now - priceMA5) * 100 / priceMA5 > 2:
            priceCondition = 1
        elif priceMA10 < latest_st_review.now < priceMA5:
            priceCondition = 3
        elif priceMA20 < latest_st_review.now < priceMA10:
            priceCondition = 5
        elif priceMA60 < latest_st_review.now < priceMA20:
            priceCondition = 7
        elif latest_st_review.now < priceMA60:
            priceCondition = 9

        all_now_prices = [s.now for s in block_st_reviews][:20]
        all_high_prices = [s.high for s in block_st_reviews][:20]
        all_low_prices = [s.low for s in block_st_reviews][:20]
        all_close_prices = [s.open for s in block_st_reviews][:20]
        all_volumes = [s.volume for s in block_st_reviews][:20]

        # 计算盈亏比, 从最近20天计算
        now_prices = all_now_prices[:20]
        sorted_now_prices = sorted(now_prices)
        lowest_price = sorted_now_prices[0]
        highest_price = sorted_now_prices[-1]
        profitLossRatio = 0
        profitRate = 0

        recent3_now_prices = all_now_prices[:3]
        highest3_price = max(recent3_now_prices)
        recent5_now_prices = all_now_prices[:5]
        highest5_price = max(recent5_now_prices)
        recent10_now_prices = all_now_prices[:10]
        highest10_price = max(recent10_now_prices)
        recent20_now_prices = all_now_prices[:20]
        highest20_price = max(recent20_now_prices)

        last3UpRate = (recent3_now_prices[0] - recent3_now_prices[-1]) * 100 / recent3_now_prices[-1]
        last5UpRate = (recent5_now_prices[0] - recent5_now_prices[-1]) * 100 / recent5_now_prices[-1]
        last10UpRate = (recent10_now_prices[0] - recent10_now_prices[-1]) * 100 / recent10_now_prices[-1]
        last20UpRate = (recent20_now_prices[0] - recent20_now_prices[-1]) * 100 / recent20_now_prices[-1]
        breakUpRecent3HighestPrice = 1 if latest_st_review.now > highest3_price else 0
        breakUpRecent5HighestPrice = 1 if latest_st_review.now > highest5_price else 0
        breakUpRecent10HighestPrice = 1 if latest_st_review.now > highest10_price else 0
        breakUpRecent20HighestPrice = 1 if latest_st_review.now > highest20_price else 0

        if latest_st_review.code == '002594':
            print('test')
        lossRate = 0
        if latest_st_review.now > lowest_price and latest_st_review.now < highest_price:
            profitLossRatio = (highest_price - latest_st_review.now) / (latest_st_review.now - lowest_price)
            profitRate = (highest_price - latest_st_review.now) * 100 / latest_st_review.now
            lossRate = (lowest_price - latest_st_review.now) * 100 / latest_st_review.now

        return StockStatistics(
            code=latest_st_review.code,
            priceMA5=priceMA5,
            priceMA10=priceMA10,
            priceMA20=priceMA20,
            priceMA60=priceMA60,
            volMA5=volMA5,
            volMA10=volMA10,
            volMA20=volMA20,
            volMA40=volMA40,
            volMA60=volMA60,
            volMA145=volMA145,
            volCondition=volCondition,
            priceCondition=priceCondition,
            volContinueCondition=volContinueCondition,
            last3UpRate=last3UpRate,
            last5UpRate=last5UpRate,
            last10UpRate=last10UpRate,
            last20UpRate=last20UpRate,
            breakUpRecent3HighestPrice=breakUpRecent3HighestPrice,
            breakUpRecent5HighestPrice=breakUpRecent5HighestPrice,
            breakUpRecent10HighestPrice=breakUpRecent10HighestPrice,
            breakUpRecent20HighestPrice=breakUpRecent20HighestPrice,
            profitLossRatio=profitLossRatio,
            profitRate=profitRate,
            lossRate=lossRate,
            recentNowPrices=json.dumps(all_now_prices),
            recentHighPrices=json.dumps(all_high_prices),
            recentLowPrices=json.dumps(all_low_prices),
            recentClosePrices=json.dumps(all_close_prices),
            recentVolumes=all_volumes,
            createdAt=late_day
        )

    def handle(self, *args, **options):
        now = datetime.datetime.now()

        stock_reviews = StockReviewRecent60.objects \
            .order_by('code', '-createdAt') \
            .exclude(code__istartswith='30') \
            .exclude(code__istartswith='688') \
            .exclude(name__startswith='*ST') \
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
                    if stock_statistics:
                        stock_statistics_arr.append(stock_statistics)
                    block_st_reviews = [stock_review]
            else:
                block_st_reviews.append(stock_review)

            pre_st_review = stock_review

        StockStatistics.objects.all().delete()

        StockStatistics.objects.bulk_create(stock_statistics_arr)
