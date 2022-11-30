import json
from datetime import datetime, timedelta

import easyquotation
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from settings import GOLDEN_RATIOS
from stock.models import Stock, StockFundamental, MyStock, BidHistory, BidSentimentHistory, \
    DailyLimitLevel1Stock
from stock.serializer import StockFundamentalSerializer, StockSerializer


def index(request):
    return render(request, 'index.html')


def all_stock_list(request):
    code = request.GET.get('code')
    name = request.GET.get('name')
    market = request.GET.get('market')
    category = request.GET.get('category')
    type = request.GET.get('type')
    pageSize = int(request.GET.get('pageSize') or '20')
    current = int(request.GET.get('current') or '1')

    stocks = Stock.objects.order_by('id')
    if code:
        stocks = stocks.filter(code=code)
    if name:
        stocks = stocks.filter(name__icontains=name)

    if market:
        stocks = stocks.filter(market__icontains=market)

    if category:
        stocks = stocks.filter(category__icontains=category)

    if type:
        stocks = stocks.filter(type__icontains=type)

    count = stocks.count()

    stocks = stocks[(current - 1) * pageSize: (current - 1) * pageSize + pageSize]
    serializer = StockSerializer(stocks, many=True)
    data = {
        "code": 0,
        "msg": "success",
        "data": {
            "list": serializer.data,
            "total": count,

        }
    }
    return JsonResponse(data, safe=False)


def all_stock_fundamental_list(request):
    code = request.GET.get('code')
    name = request.GET.get('name')
    turnover_rate_low = int(request.GET.get('turnoverRateLow') or '-1')
    turnover_rate_high = int(request.GET.get('turnoverRateHigh') or '-1')
    stock_fundamentals = StockFundamental.objects.order_by('-turnoverRate')
    if code:
        stock_fundamentals = stock_fundamentals.filter(code=code)
    if name:
        stock_fundamentals = stock_fundamentals.filter(name__icontains=name)

    if turnover_rate_low >= 0:
        stock_fundamentals = stock_fundamentals.filter(turnoverRate__gte=turnover_rate_low)

    if turnover_rate_high >= 0:
        stock_fundamentals = stock_fundamentals.filter(turnoverRate__lte=turnover_rate_high)

    count = stock_fundamentals.count()

    serializer = StockFundamentalSerializer(stock_fundamentals, many=True)
    data = {
        "code": 0,
        "msg": "success",
        "data": {
            "list": serializer.data,
            "total": count,

        }
    }
    return JsonResponse(data, safe=False)


def my_stock_list(request):
    quotation = easyquotation.use('tencent')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

    my_stocks = MyStock.objects.order_by('-visible', '-id').all()
    codes = [stock.code for stock in my_stocks]
    real_result = quotation.real(codes)

    result = []
    for stock in my_stocks:
        detail = real_result[stock.code]
        lowest = stock.lowestPrice
        pressure_prices = [round(lowest * (1 + ratio), 2) for ratio in GOLDEN_RATIOS]
        result.append({
            'code': stock.code,
            'name': detail['name'],
            'buyPrice': stock.buyPrice,
            'safePrice': stock.safePrice,
            'now': detail['now'],
            'open': detail['open'],
            'high': detail['high'],
            'low': detail['low'],
            'needAlert': ((detail['now'] - detail['open']) * 100 / detail['open']) > 2.9,
            'turnoverRate': detail['turnover'],
            'pressurePrices': pressure_prices,
            'buyDate': stock.buyDate.strftime("%Y-%m-%d %H:%M:%S"),
            'detailUrl': 'http://stockpage.10jqka.com.cn/%s/' % stock.code,
        })
    data = {
        "code": 0,
        "data": {
            "list": result
        }
    }
    response = HttpResponse(json.dumps(data))
    return response


def my_stock_create(request):
    body_unicode = request.body.decode('utf-8')
    params = json.loads(body_unicode)

    code = params.get('code')
    buyPrice = params.get('buyPrice')
    safePrice = params.get('safePrice')
    buyReason = params.get('buyReason')

    stock = Stock.objects.filter(code=code).first()
    if stock:
        pass
        my_stock = MyStock()
        my_stock.code = stock.code
        my_stock.name = stock.name
        my_stock.buyPrice = buyPrice
        my_stock.safePrice = safePrice
        my_stock.buyReason = buyReason
        my_stock.save()

    response = HttpResponse(json.dumps({}))
    return response

def recommend_stock_list(request):
    now = datetime.now()
    bid_end_time = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                   microseconds=now.microsecond) + timedelta(hours=9, minutes=25, seconds=1)
    bid_histories = BidHistory.objects.filter(bidTime__gte=bid_end_time, openHigh__gt=2).order_by('openHigh',
                                                                                                  'industry')

    records = []
    for bid_history in bid_histories:
        records.append({
            'code': bid_history.code,
            'name': bid_history.name,
            'type': bid_history.type,
            'industry': bid_history.industry,
            'concepts': '/'.join(json.loads(bid_history.concepts)),
            'openHigh': bid_history.openHigh,
            'open': bid_history.open,
            'close': bid_history.close,
            'now': bid_history.now,
            'openHighRate': (bid_history.open - bid_history.close) * 100 / bid_history.close,
            'detailUrl': 'http://stockpage.10jqka.com.cn/%s/' % bid_history.code,
            'closeMoney': '%d.2亿' % bid_history.bid1Money
        })

    records.sort(key=lambda x: x['openHighRate'])

    data = {
        "code": 0,
        "data": {
            "list": records
        }
    }
    response = HttpResponse(json.dumps(data, ensure_ascii=False))
    return response


def recommend_industry_list(request):
    now = datetime.now()
    bid_end_time1 = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                    microseconds=now.microsecond) + timedelta(hours=9, minutes=15, seconds=0)
    bid_end_time2 = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                    microseconds=now.microsecond) + timedelta(hours=9, minutes=20, seconds=0)
    bid_end_time3 = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                    microseconds=now.microsecond) + timedelta(hours=9, minutes=25, seconds=0)
    sentimental_histories = BidSentimentHistory.objects.filter(bidTime__gte=bid_end_time1)\
        .order_by('industry', '-count')

    records = []
    for sentimental_history in sentimental_histories:
        records.append({
            'industry': sentimental_history.industry,
            'count': sentimental_history.count,
            'bidTime': sentimental_history.bidTime.strftime("%Y-%m-%d %H:%M:%S"),
        })

    data = {
        "code": 0,
        "data": {
            "list": records
        }
    }
    response = HttpResponse(json.dumps(data, ensure_ascii=False))
    return response


def daily_limit_stocks(request):
    quotation = easyquotation.use('tencent')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

    all_daily_limit_stocks = DailyLimitLevel1Stock.objects.order_by('-visible', '-id').all()
    codes = [stock.code for stock in my_stocks]
    real_result = quotation.real(codes)

    result = []
    for stock in my_stocks:
        detail = real_result[stock.code]
        lowest = stock.lowestPrice
        pressure_prices = [round(lowest * (1 + ratio), 2) for ratio in GOLDEN_RATIOS]
        result.append({
            'code': stock.code,
            'name': detail['name'],
            'buyPrice': stock.buyPrice,
            'safePrice': stock.safePrice,
            'now': detail['now'],
            'open': detail['open'],
            'high': detail['high'],
            'low': detail['low'],
            'needAlert': ((detail['now'] - detail['open']) * 100 / detail['open']) > 2.9,
            'turnoverRate': detail['turnover'],
            'pressurePrices': pressure_prices,
            'buyDate': stock.buyDate.strftime("%Y-%m-%d %H:%M:%S"),
            'detailUrl': 'http://stockpage.10jqka.com.cn/%s/' % stock.code,
        })
    data = {
        "code": 0,
        "data": {
            "list": result
        }
    }
    response = HttpResponse(json.dumps(data))
    return response