import easyquotation
from django.core.management.base import BaseCommand

from stock.util.ashare import *


class IndustryItem(object):
    industry = ''
    stocks = []

    def __init__(self, industry, stocks):
        self.industry = industry
        self.stocks = stocks

from futu import *
class AdditionalNum(object):
    value = 0.0
    idx = 0
    is_inflection = False

    def __init__(self, value, idx):
        self.value = value
        self.idx = idx


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        # 初始化pro接口
        # df = get_price('sh880491', frequency='1d', count=5)  # 默认获取今天往前5天的日线实时行情
        # print('上证指数日线行情\n', df)

        # quotation = easyquotation.use('jsl') # ['jsl']
        # res = quotation.funda()
        #
        # real_result = quotation.real(['000001'])
        # print(real_result)


        import akshare as ak
        stock_board_concept_index_ths_df = ak.stock_board_concept_index_ths_df(symbol="丙烯酸")
        print(stock_board_concept_index_ths_df)

