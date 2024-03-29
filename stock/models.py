from django.db import models


class Stock(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)  # 代码
    name = models.CharField(max_length=64)  # 名称
    market = models.CharField(max_length=64)  # 名称
    category = models.CharField(max_length=64)  # 名称
    type = models.CharField(max_length=64)  # 名称
    industry = models.CharField(max_length=64)
    concepts = models.CharField(max_length=1024)
    marketingTime = models.CharField(max_length=64)
    marketingPlace = models.CharField(max_length=64)
    issuePrice = models.CharField(max_length=8)
    underWriter = models.CharField(max_length=64)
    regCapital = models.CharField(max_length=64)
    regPlace = models.CharField(max_length=64)
    regOfficePlace = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    mainBusiness = models.CharField(max_length=1024)
    establishTime = models.CharField(max_length=64)

    class Meta:
        db_table = "stock"


class StockIndustry(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)  # 代码
    name = models.CharField(max_length=64)  # 名称

    class Meta:
        db_table = "stock_industry"


class StockFundamental(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)  # 代码
    name = models.CharField(max_length=64)  # 名称
    marketValue = models.FloatField()  # 市值
    tradingMarketValue = models.FloatField()  # 流值
    open = models.FloatField()  # 开盘价
    high = models.FloatField()  # 最高价
    low = models.FloatField()  # 最低价
    close = models.FloatField()
    pe = models.FloatField()  # 市盈率
    turnoverRate = models.FloatField()  # 转手率
    turnoverVolume = models.IntegerField()  # 转手亮
    tradingMoney = models.FloatField()  # 交易量
    createdAt = models.DateTimeField()
    growthRate = models.FloatField()

    class Meta:
        db_table = "stock_fundamental"


class MyStock(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)  # 代码
    name = models.CharField(max_length=64)  # 名称
    buyPrice = models.FloatField()  # 市值
    buyDate = models.DateTimeField()  # 流值
    safePrice = models.FloatField()
    buyReason = models.CharField(max_length=256)  # 转手率
    sellPrice = models.FloatField()
    sellReason = models.CharField(max_length=128)  # 转手亮
    visible = models.IntegerField(default=1)
    buyVolume = models.IntegerField(default=100)

    lowestPrice = models.FloatField()
    highestPrice = models.FloatField

    class Meta:
        db_table = "my_stock"


class DailyLimitLevel1Stock(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)  # 代码
    name = models.CharField(max_length=64)  # 名称
    now = models.FloatField()
    open = models.FloatField()  # 市值
    close = models.FloatField()  # 流值
    buyPrice = models.FloatField()  # 市值
    buyDate = models.DateTimeField()  # 流值
    safePrice = models.FloatField()
    buyReason = models.CharField(max_length=256)  # 转手率
    sellPrice = models.FloatField()
    sellReason = models.CharField(max_length=128)  # 转手亮
    visible = models.IntegerField(default=1)
    type = models.CharField(max_length=64)  # 名称
    industry = models.CharField(max_length=64)
    concepts = models.CharField(max_length=1024)
    lowestPrice = models.FloatField()
    highestPrice = models.FloatField()
    growthRate = models.FloatField()

    class Meta:
        db_table = "daily_limit_level1_stock"


class DailyLimitLevel2Stock(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)  # 代码
    name = models.CharField(max_length=64)  # 名称
    now = models.FloatField()
    open = models.FloatField()  # 市值
    close = models.FloatField()  # 流值
    buyPrice = models.FloatField()  # 市值
    buyDate = models.DateTimeField()  # 流值
    safePrice = models.FloatField()
    buyReason = models.CharField(max_length=256)  # 转手率
    sellPrice = models.FloatField()
    sellReason = models.CharField(max_length=128)  # 转手亮
    visible = models.IntegerField(default=1)
    type = models.CharField(max_length=64)  # 名称
    industry = models.CharField(max_length=64)
    concepts = models.CharField(max_length=1024)
    lowestPrice = models.FloatField()
    highestPrice = models.FloatField()
    growthRate = models.FloatField()

    class Meta:
        db_table = "daily_limit_level2_stock"


class BidHistory(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)  # 代码
    name = models.CharField(max_length=64)  # 名称
    now = models.FloatField()
    open = models.FloatField()  # 市值
    close = models.FloatField()  # 流值
    type = models.CharField(max_length=64)  # 名称
    industry = models.CharField(max_length=64)
    concepts = models.CharField(max_length=1024)
    openHigh = models.IntegerField()
    bidTime = models.DateTimeField()
    bid1Money = models.FloatField()
    bid2Money = models.FloatField()
    bid3Money = models.FloatField()
    bid4Money = models.FloatField()
    bid5Money = models.FloatField()

    class Meta:
        db_table = "bid_history"


class BidSentimentHistory(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    industry = models.CharField(max_length=64)
    count = models.IntegerField()
    bidTime = models.DateTimeField()

    class Meta:
        db_table = "bid_sentiment_history"


class RecommendStock(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)  # 代码
    name = models.CharField(max_length=64)  # 名称
    open = models.FloatField()  # 市值
    preClose = models.DateTimeField()  # 流值

    class Meta:
        db_table = "recommend_stock"


class ManualRecommendStock(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)  # 代码
    name = models.CharField(max_length=64)  # 名称
    cancel = models.SmallIntegerField(default=0)

    class Meta:
        db_table = "manual_recommend_stock"


class ManualRecommendStockPriceHistory(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)  # 代码
    name = models.CharField(max_length=64)  # 名称
    createdAt = models.DateTimeField()
    open = models.FloatField()  # 开盘
    close = models.FloatField()  # 昨收盘
    low = models.FloatField()
    now = models.FloatField()
    high = models.FloatField()
    marketValue = models.FloatField()  # 市值
    tradingMarketValue = models.FloatField()  # 流值
    pe = models.FloatField()  # 市盈率
    turnoverRate = models.FloatField()  # 转手率
    openHigh = models.IntegerField()  # 是否高开
    openHighRate = models.FloatField()  # 高开幅度
    downRate = models.FloatField()
    riseUpRate = models.FloatField()
    nowRate = models.FloatField()
    afterHalfHourDownRate = models.FloatField()
    afterHalfHourRiseUpRate = models.FloatField()
    afterHalfHourNowRate = models.FloatField()
    closeRate = models.FloatField()
    needAlert = models.SmallIntegerField(default=0)  # 是否异动
    bid1Money = models.FloatField()

    class Meta:
        db_table = "manual_recommend_stock_price_history"


class StockReview(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    now = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    open = models.FloatField()
    close = models.FloatField()
    growthRate = models.FloatField()
    createdAt = models.DateTimeField()
    upLimit = models.FloatField()
    downLimit = models.FloatField()
    marketValue = models.FloatField()
    tradingMarketValue = models.FloatField()
    pe = models.FloatField()
    turnoverRate = models.FloatField()
    volume = models.FloatField()
    type = models.CharField(max_length=64)
    industry = models.CharField(max_length=64)
    concepts = models.CharField(max_length=1024)
    bid1Money = models.FloatField()
    upLimitType = models.IntegerField()  # 1、 涨停 2、 跌停 3、上涨 4、下跌 5、平
    everUpLimited = models.IntegerField(default=0)  # 0、没有涨停 1、曾经涨停
    breakUpLimitCount = models.IntegerField(default=0)
    continuousUpLimitCount = models.IntegerField(default=0)
    upDownStatistics = models.CharField(max_length=64, default='')
    firstUpLimitTime = models.CharField(max_length=64, default='')
    finalUpLimitTime = models.CharField(max_length=64, default='')
    smallUp = models.IntegerField(default=0)
    smallVolumeUp = models.IntegerField(default=0)
    volumeBreakUpMa5 = models.IntegerField(default=0)
    last2Up = models.IntegerField(default=0)
    last3Up = models.IntegerField(default=0)
    last5Up = models.IntegerField(default=0)

    class Meta:
        db_table = "stock_review"


class StockReviewStatistics(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    upLimitCount = models.IntegerField()
    downLimitCount = models.IntegerField()
    upCount = models.IntegerField()
    downCount = models.IntegerField()
    zeroCount = models.IntegerField()
    createdAt = models.DateTimeField()  # 流值

    class Meta:
        db_table = "stock_review_statistics"


class HourStockReview(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    now = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    open = models.FloatField()
    close = models.FloatField()
    growthRate = models.FloatField()
    createdAt = models.DateTimeField()
    upLimit = models.FloatField()
    downLimit = models.FloatField()
    marketValue = models.FloatField()
    tradingMarketValue = models.FloatField()
    pe = models.FloatField()
    turnoverRate = models.FloatField()
    volume = models.FloatField()
    type = models.CharField(max_length=64)
    industry = models.CharField(max_length=64)
    concepts = models.CharField(max_length=1024)
    bid1Money = models.FloatField()
    upLimitType = models.IntegerField()  # 1、 涨停 2、 跌停 3、上涨 4、下跌 5、平
    everUpLimited = models.IntegerField(default=0)  # 0、没有涨停 1、曾经涨停
    breakUpLimitCount = models.IntegerField(default=0)
    continuousUpLimitCount = models.IntegerField(default=0)
    upDownStatistics = models.CharField(max_length=64, default='')
    firstUpLimitTime = models.CharField(max_length=64, default='')
    finalUpLimitTime = models.CharField(max_length=64, default='')
    smallUp = models.IntegerField(default=0)
    smallVolumeUp = models.IntegerField(default=0)
    volumeBreakUpMa5 = models.IntegerField(default=0)
    last2Up = models.IntegerField(default=0)
    last3Up = models.IntegerField(default=0)
    last5Up = models.IntegerField(default=0)

    class Meta:
        db_table = "hour_stock_review"


class StockReviewRecent60(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    now = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    open = models.FloatField()
    close = models.FloatField()
    growthRate = models.FloatField()
    createdAt = models.DateTimeField()
    upLimit = models.FloatField()
    downLimit = models.FloatField()
    marketValue = models.FloatField()
    tradingMarketValue = models.FloatField()
    pe = models.FloatField()
    turnoverRate = models.FloatField()
    volume = models.FloatField()
    type = models.CharField(max_length=64)
    industry = models.CharField(max_length=64)
    concepts = models.CharField(max_length=1024)
    bid1Money = models.FloatField()
    upLimitType = models.IntegerField()  # 1、 涨停 2、 跌停 3、上涨 4、下跌 5、平
    everUpLimited = models.IntegerField(default=0)  # 0、没有涨停 1、曾经涨停
    breakUpLimitCount = models.IntegerField(default=0)
    continuousUpLimitCount = models.IntegerField(default=0)
    upDownStatistics = models.CharField(max_length=64, default='')
    firstUpLimitTime = models.CharField(max_length=64, default='')
    finalUpLimitTime = models.CharField(max_length=64, default='')
    smallUp = models.IntegerField(default=0)
    smallVolumeUp = models.IntegerField(default=0)
    volumeBreakUpMa5 = models.IntegerField(default=0)
    last2Up = models.IntegerField(default=0)
    last3Up = models.IntegerField(default=0)
    last5Up = models.IntegerField(default=0)

    class Meta:
        db_table = "stock_review_recent60"


class StockStatistics(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)

    priceMA5 = models.FloatField()
    priceMA10 = models.FloatField()
    priceMA20 = models.FloatField()
    priceMA60 = models.FloatField()

    volMA5 = models.FloatField()
    volMA10 = models.FloatField()
    volMA20 = models.FloatField()
    volMA40 = models.FloatField()
    volMA60 = models.FloatField()
    volMA145 = models.FloatField()

    # 成交量处于40日线以下，价格关键位置
    volCondition = models.IntegerField(default=0)
    # 价格处于位置，>5 10-5, 20-10, 60-20, <60
    priceCondition = models.IntegerField(default=0)
    volContinueCondition = models.IntegerField(default=0)
    last3UpRate = models.FloatField()
    last5UpRate = models.FloatField()
    last10UpRate = models.FloatField()
    last20UpRate = models.FloatField()
    breakUpRecent3HighestPrice = models.IntegerField(default=0)
    breakUpRecent5HighestPrice = models.IntegerField(default=0)
    breakUpRecent10HighestPrice = models.IntegerField(default=0)
    breakUpRecent20HighestPrice = models.IntegerField(default=0)
    profitLossRatio = models.FloatField(default=0)
    profitRate = models.FloatField(default=0)
    lossRate = models.FloatField(default=0)
    recentNowPrices = models.TextField(default='')
    recentHighPrices = models.TextField(default='')
    recentLowPrices = models.TextField(default='')
    recentClosePrices = models.TextField(default='')
    recentVolumes = models.TextField(default='')
    createdAt = models.DateTimeField()

    class Meta:
        db_table = "stock_statistics"


class IndustryBlock(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    now = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    open = models.FloatField()
    close = models.FloatField()
    growthRate = models.FloatField()
    createdAt = models.DateTimeField()
    inFlowFunds = models.FloatField()
    turnover = models.FloatField()
    volume = models.FloatField()
    upCount = models.IntegerField()
    downCount = models.IntegerField()

    class Meta:
        db_table = "industry_block"


class ConceptBlock(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    now = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    open = models.FloatField()
    close = models.FloatField()
    growthRate = models.FloatField()
    createdAt = models.DateTimeField()
    inFlowFunds = models.FloatField()
    turnover = models.FloatField()
    volume = models.FloatField()
    upCount = models.IntegerField()
    downCount = models.IntegerField()

    class Meta:
        db_table = "concept_block"


class RecommendStockInRealTime(models.Model):
    # id = models.AutoField(primary_key=True, default=1)  # id 会自动创建,可以手动写入
    code = models.CharField(max_length=16)  # 代码
    name = models.CharField(max_length=64)  # 名称
    industry = models.CharField(max_length=64)  # 名称
    createdAt = models.DateTimeField()
    marketValue = models.FloatField()  # 市值
    turnoverRate = models.FloatField()  # 转手率
    openHighRate = models.FloatField()  # 高开幅度
    bottomUpRate = models.FloatField()  # 底部拉升幅度
    nowRate = models.FloatField()
    canBuy = models.SmallIntegerField(default=0)  # 是否异动
    turnover = models.FloatField()
    recent5ProfitLossRatio = models.TextField()
    recent10ProfitLossRatio = models.TextField()
    recent20ProfitLossRatio = models.TextField()

    class Meta:
        db_table = "recommend_stock_in_real_time"
