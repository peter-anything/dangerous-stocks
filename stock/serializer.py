from rest_framework import serializers

from stock.models import StockFundamental, Stock


class StockFundamentalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(max_length=16)  # 代码
    name = serializers.CharField(max_length=64)  # 名称
    marketValue = serializers.FloatField()  # 市值
    tradingMarketValue = serializers.FloatField()  # 流值
    open = serializers.FloatField()  # 开盘价
    high = serializers.FloatField()  # 最高价
    low = serializers.FloatField()  # 最低价
    pe = serializers.FloatField()  # 市盈率
    turnoverRate = serializers.FloatField()  # 转手率
    turnoverVolume = serializers.IntegerField()  # 转手亮
    tradingMoney = serializers.FloatField()  # 交易量
    createdAt = serializers.DateTimeField(format='%Y-%m-%d')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return StockFundamental.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class StockSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(max_length=16)  # 代码
    name = serializers.CharField(max_length=64)  # 名称
    market = serializers.CharField(max_length=64)  # 名称
    category = serializers.CharField(max_length=64)  # 名称
    type = serializers.CharField(max_length=64)  # 名称

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Stock.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
