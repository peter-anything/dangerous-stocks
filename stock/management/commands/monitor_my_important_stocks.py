import easyquotation
from django.core.management.base import BaseCommand

from stock.models import Stock


class IndustryItem(object):
    industry = ''
    stocks = []

    def __init__(self, industry, stocks):
        self.industry = industry
        self.stocks = stocks


MY_IMPORTANT_STOCKS = {
    '建筑': {
        'names': ['中国交建', '中国铁建', '中国中铁', '中国建筑', '中钢国际', '中国化学'],
        'upLimit': 1.5
    },
    '游戏': {
        'names': ['三七互娱', '世纪华通', '巨人网络', '恺英网络', '完美世界', '游族网络'],
        'upLimit': 2
    },
    '煤炭': {
        'names': ['潞安环能', '中国神华', '山煤国际', '山西焦化', '恒源煤电', '冀中能源', '山煤国际'],
        'upLimit': 2
    },
    '证券': {
        'names': ['中泰证券', '华泰证券', '东方证券', '中信证券', '广发证券', '兴业证券', '中国银河'],
        'upLimit': 1
    },
    '中药': {
        'names': ['康缘药业', '方盛制药', '华润三九', '达仁堂', '康恩贝', '太极集团', '昆药集团', '健民集团'],
        'upLimit': 2
    },
    '工业母机': {
        'names': ['埃斯顿', '南兴股份', '豪迈科技', '海天精工', '秦川机床', '华工科技', '大族激光'],
        'upLimit': 2
    },
    '电力': {
        'names': ['华能国际', '华电国际', '浙能电力'],
        'upLimit': 2
    },
    '半导体设备': {
        'names': ['北方华创'],
        'upLimit': 2
    },
    '半导体材料': {
        'names': ['立昂微', '雅克科技'],
        'upLimit': 2
    },
    'CHIPLET': {
        'names': ['华天科技', '长电科技', '通富微电'],
        'upLimit': 2
    },
    'PCB': {
        'names': ['深南电路', '沪电股份', '鹏鼎控股', '兴森科技', '奥士康', '景旺电子', '崇达技术', '生益科技'],
        'upLimit': 2
    },
    '消费电子': {
        'names': ['奋达科技', '漫步者', '深科技', '工业富联', '领益智造', '环旭电子'],
        'upLimit': 2
    },
    '汽车芯片': {
        'names': ['兆易创新', '韦尔股份', '闻泰科技'],
        'upLimit': 2
    },
    '军工': {
        'names': ['海格通信', '中航电子', '航发动力', '中国船舶', '洪都航空', '国睿科技', '航天电子', '北方导航'],
        'upLimit': 2
    },
    '国资云': {
        'names': ['浪潮信息', '太极股份', '广电运通', '深桑达Ａ', '常山北明', '数据港', '杭钢股份'],
        'upLimit': 2
    },
    '人工智能': {
        'names': ['海康威视', '科大讯飞', '三六零', '恒生电子', '大华股份', '用友网络'],
        'upLimit': 2
    },
    '算力': {
        'names': ['工业富联', '拓维信息', '紫光股份', '剑桥科技', '神州数码', '中兴通讯', '中科曙光', '中国长城'],
        'upLimit': 2
    },
}


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        all_stocks = Stock.objects \
            .exclude(code__istartswith='300').exclude(code__istartswith='688').exclude(name__startswith='ST') \
            .exclude(name__startswith='*ST') \
            .filter(market='A股')

        st_name_map = {}
        for st in all_stocks:
            st_name_map[st.name] = st.code

        my_import_codes = []
        quotation = easyquotation.use('tencent')

        import tushare as tu
        result = tu.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'])
        data = tu.get_index()


        for industry, industry_detail in MY_IMPORTANT_STOCKS.items():
            industry_codes = [st_name_map[name] for name in industry_detail['names']]
            real_result = quotation.real([str(stock_code) for stock_code in industry_codes])

            industry_monitor_stocks = []
            for stock_code, detail in real_result.items():
                code = detail['code']
                name = detail['name']
                now = detail['now']
                open = detail['open']
                close = detail['close']
                high = detail['high']
                low = detail['low']
                bid_price = detail['bid1']

                max_up_limit = (now - low) * 100 / low
                if not max_up_limit >= industry_detail['upLimit']:
                    continue
                industry_monitor_stocks.append(detail)

            if len(industry_monitor_stocks) >= ((len(industry_codes) - 1) / 2 + 1) or len(industry_monitor_stocks) >= 3:
                print('%s 有行情, 包含股票: [%s]' % (industry, [st['name'] for st in industry_monitor_stocks]))