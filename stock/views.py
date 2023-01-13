import json
from datetime import datetime, timedelta

import easyquotation
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from settings import GOLDEN_RATIOS
from stock import util
from stock.models import Stock, StockFundamental, MyStock, BidHistory, BidSentimentHistory, DailyLimitLevel1Stock, \
    ManualRecommendStock, ManualRecommendStockPriceHistory, StockReview
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

    my_stocks = MyStock.objects.filter(visible=1).order_by('-visible', '-id').all()
    codes = [stock.code for stock in my_stocks]
    real_result = quotation.real(codes)

    result = []
    for stock in my_stocks:
        detail = real_result[stock.code]
        lowest = stock.lowestPrice
        pressure_prices = [round(lowest * (1 + ratio), 2) for ratio in GOLDEN_RATIOS]
        if detail['open'] > 0:
            closeMoney = detail['bid1'] * detail['bid1_volume'] / 10000000
            need_alert = ((detail['now'] - detail['open']) * 100 / detail['open']) > 2.9 or closeMoney >= 0.5
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
                'closeMoney': closeMoney,
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
    createdAt = datetime.now().strftime("%Y-%m-%d")
    manual_stock_histories = ManualRecommendStockPriceHistory.objects\
        .filter(code__in=codes)\
        .filter(bid1Money__gte=0.5)\
        .filter(createdAt__lt=createdAt + ' 23:59:59')\
        .filter(createdAt__gt=createdAt + ' 00:00:00')\
        .order_by('-needAlert', '-bid1Money')
    manual_stock_history_map = {}
    for manual_stock_history in manual_stock_histories:
        manual_stock_history_map[manual_stock_history.code] = manual_stock_history

    result = []
    already_exists_codes = {}
    for manual_stock_history in manual_stock_histories:
        stock_detail = stock_map[manual_stock_history.code]
        if not manual_stock_history.nowRate:
            continue
        if manual_stock_history.code in already_exists_codes:
            continue

        already_exists_codes[manual_stock_history.code] = True

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


def daily_stock_review(request):
    result = []
    createdAt = request.GET.get('createdAt')
    upLimitType = request.GET.get('upLimitType')
    industry = request.GET.get('industry')
    if not createdAt:
        createdAt = datetime.now().strftime("%Y-%m-%d")
    if not upLimitType:
        upLimitType = 1

    stocks = StockReview.objects.filter(upLimitType=upLimitType)
    if industry:
        stocks = stocks.filter(industry=industry)

    if createdAt:
        stocks = stocks \
            .filter(createdAt__gt=createdAt + ' 00:00:00') \
            .filter(createdAt__lt=createdAt + ' 23:59:59') \
            .order_by('-continuousUpLimitCount', 'finalUpLimitTime')

    for stock in stocks:
        result.append({
            'code': stock.code,
            'name': stock.name,
            'now': stock.now,
            'open': stock.open,
            'marketValue': stock.marketValue,
            'tradingMarketValue': stock.tradingMarketValue,
            'turnoverRate': stock.turnoverRate,
            'closeMoney': round(stock.bid1Money / 10.0, 2),
            'type': stock.type,
            'industry': stock.industry,
            'concepts': stock.concepts,
            'firstUpLimitTime': stock.firstUpLimitTime[11:],
            'finalUpLimitTime': stock.finalUpLimitTime[11:],
            'breakUpLimitCount': stock.breakUpLimitCount,
            'continuousUpLimitCount': stock.continuousUpLimitCount,
            'upDownStatistics': stock.upDownStatistics,
            'growthRate': stock.growthRate,
            'createdAt': stock.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            'detailUrl': 'http://stockpage.10jqka.com.cn/%s/' % stock.code,
        })
    data = {
        "code": 0,
        "data": {
            "list": result
        },
        'total': 0
    }
    response = HttpResponse(json.dumps(data))
    return response


def daily_stock_review_statistics(request):
    result = []
    createdAt = request.GET.get('createdAt')
    analysisType = request.GET.get('analysisType', '2')
    if not createdAt:
        createdAt = datetime.now().strftime("%Y-%m-%d")

    if analysisType == '1':
        ever_limit_up_count = StockReview.objects.filter(everUpLimited=1) \
            .filter(createdAt__gt=createdAt + ' 00:00:00') \
            .filter(createdAt__lt=createdAt + ' 23:59:59') \
            .count()

        up_limit_count = StockReview.objects.filter(upLimitType=1) \
            .filter(createdAt__gt=createdAt + ' 00:00:00') \
            .filter(createdAt__lt=createdAt + ' 23:59:59').count()

        down_limit_count = StockReview.objects.filter(upLimitType=2) \
            .filter(createdAt__gt=createdAt + ' 00:00:00') \
            .filter(createdAt__lt=createdAt + ' 23:59:59').count()

        up_count = StockReview.objects.filter(upLimitType=3)\
            .filter(createdAt__gt=createdAt + ' 00:00:00')\
            .filter(createdAt__lt=createdAt + ' 23:59:59').count()

        down_count = StockReview.objects.filter(upLimitType=4) \
            .filter(createdAt__gt=createdAt + ' 00:00:00') \
            .filter(createdAt__lt=createdAt + ' 23:59:59').count()

        zero_count = StockReview.objects.filter(upLimitType=5) \
            .filter(createdAt__gt=createdAt + ' 00:00:00') \
            .filter(createdAt__lt=createdAt + ' 23:59:59').count()

        result = []

        result.append({
            'key': '上涨数',
            'value': up_count
        })
        result.append({
            'key': '下跌数',
            'value': down_count
        })
        result.append({
            'key': '涨停数',
            'value': up_limit_count
        })
        result.append({
            'key': '跌停数',
            'value': down_limit_count
        })
        result.append({
            'key': '平家数',
            'value': zero_count
        })
        result.append({
            'key': '曾涨停数',
            'value': ever_limit_up_count
        })
        result.append({
            'key': '涨停封板率',
            'value': up_limit_count / (up_limit_count + ever_limit_up_count)
        })

        stocks = StockReview.objects \
            .filter(createdAt__gt=createdAt + ' 00:00:00') \
            .filter(createdAt__lt=createdAt + ' 23:59:59') \
            .all()

        up_limit_1_count = 0
        up_limit_2_count = 0
        up_limit_3_count = 0
        up_limit_4_count = 0
        up_limit_5_count = 0
        up_limit_6_count = 0
        up_limit_7_count = 0
        up_limit_8_count = 0
        up_limit_9_count = 0
        up_limit_10_count = 0
        up_limit_10_plus_count = 0
        for st in stocks:
            if st.continuousUpLimitCount == 1:
                up_limit_1_count += 1
            elif st.continuousUpLimitCount == 2:
                up_limit_2_count += 1
            elif st.continuousUpLimitCount == 3:
                up_limit_3_count += 1
            elif st.continuousUpLimitCount == 4:
                up_limit_4_count += 1
            elif st.continuousUpLimitCount == 5:
                up_limit_5_count += 1
            elif st.continuousUpLimitCount == 6:
                up_limit_6_count += 1
            elif st.continuousUpLimitCount == 7:
                up_limit_7_count += 1
            elif st.continuousUpLimitCount == 8:
                up_limit_8_count += 1
            elif st.continuousUpLimitCount == 9:
                up_limit_9_count += 1
            elif st.continuousUpLimitCount == 10:
                up_limit_10_count += 1
            else:
                up_limit_10_plus_count += 1
        result.append({
            'key': '一板数',
            'value': up_limit_1_count
        })
        result.append({
            'key': '二板数',
            'value': up_limit_2_count
        })
        result.append({
            'key': '三板数',
            'value': up_limit_3_count
        })
        result.append({
            'key': '四板数',
            'value': up_limit_4_count
        })
        result.append({
            'key': '五板数',
            'value': up_limit_5_count
        })
        result.append({
            'key': '六板数',
            'value': up_limit_6_count
        })
        result.append({
            'key': '七板数',
            'value': up_limit_7_count
        })
        result.append({
            'key': '八板数',
            'value': up_limit_8_count
        })
        result.append({
            'key': '九板数',
            'value': up_limit_9_count
        })
        result.append({
            'key': '十板数',
            'value': up_limit_10_count
        })
        result.append({
            'key': '十板以上',
            'value': up_limit_10_plus_count
        })
    elif analysisType == '2':
        stocks = StockReview.objects \
            .filter(createdAt__gt=createdAt + ' 00:00:00') \
            .filter(createdAt__lt=createdAt + ' 23:59:59') \
            .all()
        industry_map = {}
        for stock in stocks:
            industry_detail = None
            if not stock.industry:
                continue
            if stock.industry in industry_map:
                industry_detail = industry_map[stock.industry]
            else:
                industry_detail = {
                    '涨停数': 0,
                    '跌停数': 0,
                    '曾涨停数': 0,
                    '上涨数': 0,
                    '下跌数': 0,
                    '平家数': 0,
                    '上涨率': 0
                }
                industry_map[stock.industry] = industry_detail

            if stock.upLimitType == 1:
                industry_detail['涨停数'] = industry_detail['涨停数'] + 1
            elif stock.upLimitType == 2:
                industry_detail['跌停数'] = industry_detail['跌停数'] + 1
            elif stock.upLimitType == 3:
                industry_detail['上涨数'] = industry_detail['上涨数'] + 1
            elif stock.upLimitType == 4:
                industry_detail['下跌数'] = industry_detail['下跌数'] + 1
            elif stock.upLimitType == 5:
                industry_detail['平家数'] = industry_detail['平家数'] + 1
            elif stock.everUpLimited == 1:
                industry_detail['曾涨停数'] = industry_detail['曾涨停数'] + 1
            industry_map[stock.industry] = industry_detail

            for industry, detail in industry_map.items():
                if (industry_map[industry]['涨停数'] + industry_map[industry]['跌停数'] + industry_map[industry]['上涨数'] + industry_map[industry]['下跌数'] + industry_map[industry]['平家数']) > 10:
                    industry_map[industry]['上涨率'] = (industry_map[industry]['涨停数'] + industry_map[industry]['上涨数'] ) * 100 / (industry_map[industry]['涨停数'] + industry_map[industry]['跌停数'] + industry_map[industry]['上涨数'] + industry_map[industry]['下跌数'] + industry_map[industry]['平家数'])

        for industry, detail in industry_map.items():
            result.append({
                'key': industry,
                'value': detail
            })

        result.sort(key=lambda x: x['value']['涨停数'], reverse=True)
        for idx, r in enumerate(result):
            r['value'] = json.dumps(r['value']).encode().decode('unicode-escape')
            result[idx] = r

    data = {
        "code": 0,
        "data": {
            "list": result
        },
    }
    response = HttpResponse(json.dumps(data))
    return response
