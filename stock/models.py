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

    lowestPrice = models.FloatField()
    highestPrice = models.FloatField

    class Meta:
        db_table = "my_stock"


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
