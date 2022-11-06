# 获取全部股票代码及名称
import logging

# 获取股票信息
import requests


def _get_stocks(base_url, stock):
    max_page_num = 50
    page_size = 100
    result = []

    for page_num in range(1, max_page_num):
        url = base_url.format(time_id=stock["time_id"], page_num=page_num, page_size=page_size)
        resp = requests.get(url)

        if not resp.ok:
            logging.error("{0}-{1}-{2}请求失败：{3}".format(stock["type"],
                                                       stock["category"],
                                                       stock["tag"],
                                                       url))

        resp_json = resp.json()
        if not resp_json["data"]:
            logging.warning("当前页无数据，将不再继续请求！")
            break

        stocks = resp_json["data"]["diff"]
        result.extend(list(
            map(lambda s: {"id": s["f12"].replace(" ", "").replace("'", "_"),
                           "name": s["f14"].replace(" ", "").replace("'", "_"),
                           "category": stock["category"],
                           "tag": stock["tag"],
                           "type": stock["type"]},
                stocks)))

    logging.info("{0}-{1}-{2}信息爬取完成，共{3}条。".format(stock["type"], stock["category"], stock["tag"], len(result)))
    return result


def _get_all_stocks():
    base_url = "http://54.push2.eastmoney.com/api/qt/clist/get?pn={page_num}&pz={page_size}&po=1&np=1&fltt=2&invt=2&fid=f3&fs={time_id}&fields=f12,f14"
    stocks = [
        {
            "category": "A股",
            "tag": "沪深A股",
            "type": "股票",
            "time_id": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23"
        },
        {
            "category": "A股",
            "tag": "上证A股",
            "type": "股票",
            "time_id": "m:1+t:2,m:1+t:23"
        },
        {
            "category": "A股",
            "tag": "深证A股",
            "type": "股票",
            "time_id": "m:0+t:6,m:0+t:80"
        },
        {
            "category": "A股",
            "tag": "新股",
            "type": "股票",
            "time_id": "m:0+f:8,m:1+f:8"
        },
        {
            "category": "A股",
            "tag": "创业板",
            "type": "股票",
            "time_id": "m:0+t:80"
        },
        {
            "category": "A股",
            "tag": "科创板",
            "type": "股票",
            "time_id": "m:1+t:23"
        },
        {
            "category": "A股",
            "tag": "沪股通",
            "type": "股票",
            "time_id": "b:BK0707"
        },
        {
            "category": "A股",
            "tag": "深股通",
            "type": "股票",
            "time_id": "b:BK0804"
        },
        {
            "category": "B股",
            "tag": "B股",
            "type": "股票",
            "time_id": "m:0+t:7,m:1+t:3"
        },
        {
            "category": "A-B股",
            "tag": "上证AB股比价",
            "type": "股票",
            "time_id": "m:1+b:BK0498"
        },
        {
            "category": "A-B股",
            "tag": "深证AB股比价",
            "type": "股票",
            "time_id": "m:0+b:BK0498"
        },
        {
            "category": "A-B股",
            "tag": "风险警示板",
            "type": "股票",
            "time_id": "m:0+f:4,m:1+f:4"
        },
        {
            "category": "A-B股",
            "tag": "两网及退市",
            "type": "股票",
            "time_id": "m:0+s:3"
        },
        {
            "category": "美股",
            "tag": "美股",
            "type": "股票",
            "time_id": "m:105,m:106,m:107"
        },
        {
            "category": "港股",
            "tag": "港股",
            "type": "股票",
            "time_id": "m:128+t:3,m:128+t:4,m:128+t:1,m:128+t:2"
        },
        {
            "category": "英股",
            "tag": "英股",
            "type": "股票",
            "time_id": "m:155+t:1,m:155+t:2,m:155+t:3,m:156+t:1,m:156+t:2,m:156+t:5,m:156+t:6,m:156+t:7,m:156+t:8"
        }
    ]

    all_stocks = []
    for stock in stocks:
        all_stocks.extend(_get_stocks(base_url, stock))

    logging.warning("全部股票信息共{0}条。".format(len(all_stocks)))
    return all_stocks


# 保存股票信息至本地
def save_stocks():
    all_stocks = _get_all_stocks()
    with open("stock.csv", 'a+', encoding='utf-8') as f:
        f.write("股票代码,股票名称,市场,分类,类型\n")
        for stock in all_stocks:
            f.write("{stock[id]},{stock[name]},{stock[category]},{stock[tag]},{stock[type]}\n".format(
                stock=stock
            ))

    logging.info("全部股票信息写入完成！")


if __name__ == "__main__":
    save_stocks()
