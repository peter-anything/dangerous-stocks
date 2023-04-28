from stock.models import StockStatistics, StockReview


def get_stock_statistics_map(date_min, date_max):
    stock_statistics = StockStatistics.objects.filter(createdAt__lt=date_max, createdAt__gt=date_min).all()
    ss_map = {}
    for ss in stock_statistics:
        ss_map[ss.code] = ss

    return ss_map


def gen_stock_review(detail, stock_map, createdAt):
    code = detail['code']
    name = detail['name']
    now = detail['now']
    open = detail['open']
    close = detail['close']
    high = detail['high']
    low = detail['low']
    bid_price = detail['bid1']


    if open > 0 and close > 0:
        grow_rate = (now - close) * 100 / close

        stock_review = StockReview()
        stock_review.code = code
        stock_review.name = name
        stock_review.open = open
        stock_review.close = close
        stock_review.high = high
        stock_review.low = low
        stock_review.now = now
        stock_review.createdAt = createdAt
        stock_review.marketValue = detail['总市值']
        stock_review.volume = detail['成交量(手)']
        stock_review.tradingMarketValue = detail['流通市值']
        stock_review.turnoverRate = detail['turnover']
        stock_review.turnover = detail['成交额(万)']
        stock_review.pe = detail['PE']
        stock_review.upLimit = detail['涨停价']
        stock_review.downLimit = detail['跌停价']

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

            stock_review.industry = stock_map[code].industry
            stock_review.concepts = stock_map[code].concepts
            stock_review.type = stock_map[code].type
            stock_review.growthRate = grow_rate
            stock_review.bid1Money = detail['bid1'] * detail['bid1_volume'] / 10000000

            return stock_review
