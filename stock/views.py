import json
from datetime import datetime, timedelta

import easyquotation
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from settings import GOLDEN_RATIOS
from stock import util
from stock.models import Stock, StockFundamental, MyStock, BidHistory, BidSentimentHistory, DailyLimitLevel1Stock, \
    ManualRecommendStock, ManualRecommendStockPriceHistory
from stock.serializer import StockFundamentalSerializer, StockSerializer


scheduler = BackgroundScheduler()
scheduler.add_job(util.generate_most_popular_industries, 'interval', seconds=10)
scheduler.add_job(util.generate_manual_recommend_stock_price_history, 'interval', seconds=3)
scheduler.start()


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


def alert_stocks(request):
    quotation = easyquotation.use('tencent')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

    my_stocks = MyStock.objects.order_by('-visible', '-id').all()
    codes = [stock.code for stock in my_stocks]
    real_result = quotation.real(codes)

    result = []
    for stock in my_stocks:
        detail = real_result[stock.code]
        lowest = stock.lowestPrice
        pressure_prices = [round(lowest * (1 + ratio), 2) for ratio in GOLDEN_RATIOS]
        need_alert = ((detail['now'] - detail['open']) * 100 / detail['open']) > 2.9
        result.append({
            'code': stock.code,
            'name': detail['name'],
            'buyPrice': stock.buyPrice,
            'safePrice': stock.safePrice,
            'now': detail['now'],
            'profit': (detail['now'] - stock.buyPrice) * stock.buyVolume if stock.buyVolume else 0,
            'open': detail['open'],
            'high': detail['high'],
            'low': detail['low'],
            'needAlert': need_alert,
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
        need_alert = ((detail['now'] - detail['open']) * 100 / detail['open']) > 2.9
        result.append({
            'code': stock.code,
            'name': detail['name'],
            'buyPrice': stock.buyPrice,
            'safePrice': stock.safePrice,
            'now': detail['now'],
            'profit': (detail['now'] - stock.buyPrice) * stock.buyVolume if stock.buyVolume else 0,
            'open': detail['open'],
            'high': detail['high'],
            'low': detail['low'],
            'needAlert': need_alert,
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
    lowestPrice = params.get('lowestPrice')
    buyVolume = params.get('buyVolume')

    stock = Stock.objects.filter(code=code).first()
    if stock:
        my_stock = MyStock()
        my_stock.code = stock.code
        my_stock.name = stock.name
        my_stock.buyPrice = buyPrice
        my_stock.safePrice = buyPrice
        my_stock.buyReason = buyReason
        my_stock.lowestPrice = buyPrice
        my_stock.buyVolume = buyVolume
        my_stock.save()

    response = HttpResponse(json.dumps({}))
    return response


def recommend_stock_list(request):
    now = datetime.now()
    bid_end_time = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                   microseconds=now.microsecond) + timedelta(hours=9, minutes=25, seconds=1)
    bid_histories = BidHistory.objects.filter(bidTime__gte=bid_end_time, openHigh__gt=2).order_by('openHigh',
                                                                                                  'industry')
    codes = [bid_history.code for bid_history in bid_histories]

    quotation = easyquotation.use('tencent')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
    real_result = quotation.real(codes)
    records = []
    for bid_history in bid_histories:
        now_price = real_result[bid_history.code]['now']
        # if real_result[bid_history.code]['总市值'] >= 300:
        #     continue
        records.append({
            'code': bid_history.code,
            'name': bid_history.name,
            'type': bid_history.type,
            'industry': bid_history.industry,
            'concepts': '/'.join(json.loads(bid_history.concepts)) if bid_history.concepts else '',
            'openHigh': bid_history.openHigh,
            'open': bid_history.open,
            'close': bid_history.close,
            'marketValue': real_result[bid_history.code]['总市值'],
            'now': bid_history.now,
            'openHighRate': (bid_history.open - bid_history.close) * 100 / bid_history.close,
            'nowGrowthRate': (now_price - bid_history.close) * 100 / bid_history.close,
            'detailUrl': 'http://stockpage.10jqka.com.cn/%s/' % bid_history.code,
            'closeMoney': '%d.2亿' % bid_history.bid1Money
        })

    records.sort(key=lambda x: x['nowGrowthRate'])

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
    sentimental_histories = BidSentimentHistory.objects.filter(bidTime__gte=bid_end_time1) \
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
    codes = [stock.code for stock in all_daily_limit_stocks]
    real_result = quotation.real(codes)

    result = []
    for stock in all_daily_limit_stocks:
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


def manual_recommend_stock_create(request):
    body_unicode = request.body.decode('utf-8')
    params = json.loads(body_unicode)

    code = params.get('code')

    stock = Stock.objects.filter(code=code).first()
    if stock:
        manual_recommend_stock = ManualRecommendStock()
        manual_recommend_stock.code = stock.code
        manual_recommend_stock.name = stock.name
        manual_recommend_stock.save()

    response = HttpResponse(json.dumps({}))
    return response


def manual_recommend_stocks(request):
    manual_stocks = ManualRecommendStock.objects.all()
    codes = [manual_stock.code for manual_stock in manual_stocks]
    stocks = Stock.objects.filter(code__in=codes)
    stock_map = {}
    for stock in stocks:
        stock_map[stock.code] = stock
    manual_stock_histories = ManualRecommendStockPriceHistory.objects\
        .filter(code__in=codes).filter(bid1Money__gte=0.5).order_by('-needAlert', '-bid1Money')
    manual_stock_history_map = {}
    for manual_stock_history in manual_stock_histories:
        manual_stock_history_map[manual_stock_history.code] = manual_stock_history

    result = []
    for manual_stock_history in manual_stock_histories:
        stock_detail = stock_map[manual_stock_history.code]
        result.append({
            'code': manual_stock_history.code,
            'name': manual_stock_history.name,
            'now': manual_stock_history.now,
            'industry': stock_detail.industry,
            'concepts': stock_detail.concepts,
            'type': stock_detail.type,
            'open': manual_stock_history.open,
            'high': manual_stock_history.high,
            'low': manual_stock_history.low,
            'close': manual_stock_history.close,
            'downRate': manual_stock_history.downRate,
            'riseUpRate': manual_stock_history.riseUpRate,
            'openHighRate': manual_stock_history.openHighRate,
            'closeMoney': manual_stock_history.bid1Money,
            'marketValue': manual_stock_history.marketValue,
            'tradingMarketValue': manual_stock_history.tradingMarketValue,
            'pe': manual_stock_history.pe,
            'turnoverRate': manual_stock_history.turnoverRate,
            'nowRate': manual_stock_history.nowRate,
            'afterHalfHourRiseUpRate': manual_stock_history.afterHalfHourRiseUpRate,
            'afterHalfHourDownRate': manual_stock_history.afterHalfHourDownRate,
            'afterHalfHourNowRate': manual_stock_history.afterHalfHourNowRate,
            'needAlert': manual_stock_history.needAlert,
            'detailUrl': 'http://stockpage.10jqka.com.cn/%s/' % manual_stock_history.code,
        })
    data = {
        "code": 0,
        "data": {
            "list": result
        }
    }
    response = HttpResponse(json.dumps(data))
    return response

