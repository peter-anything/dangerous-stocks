from time import sleep

import easyquotation
quotation = easyquotation.use('tencent') # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

# result = quotation.market_snapshot(prefix=True) # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀
my_stocks = {
    '002758': 15.947,
    '002119': 13.657,
    '603232': 17.032,
    '603933': 10.427,
}


while True:
    real_result = quotation.real(list(my_stocks.keys()))
    for stock, detail in real_result.items():
        print('stock: %s' % stock)
        print(detail['name'])
        print(detail['now'])
        print(my_stocks[stock])
        print(detail['now'] - my_stocks[stock])
        print((detail['now'] - my_stocks[stock]) * 100 / my_stocks[stock])
        if detail['now'] - my_stocks[stock] < 0:
            print("error =================================")
    sleep(10)

