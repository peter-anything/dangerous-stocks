import json

import easyquotation
from django.http import HttpResponse
from django.shortcuts import render

from current_stocks import my_stocks


def index(request):
    return render(request, 'index.html')


def stock_list(request):
    quotation = easyquotation.use('tencent') # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
    real_result = quotation.real(list(my_stocks.keys()))

    result = []
    for stock_code, detail in real_result.items():
        result.append({
            'code': stock_code,
            'name': detail['name'],
            'buyPrice': my_stocks[stock_code],
            'nowPrice': detail['now']

        })
    data = {
        "code": 0,
        "data": {
            "list": result
        }
    }
    response = HttpResponse(json.dumps(data))
    response['Access-Control-Allow-Origin'] = '*'  #  其实加这一个响应参数就行
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response['Access-Control-Max-Age'] = '1000'
    response['Access-Control-Allow-Headers'] = '*'
    return response