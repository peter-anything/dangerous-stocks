import datetime

import tushare as ts
from bulk_update.helper import bulk_update
from django.core.management.base import BaseCommand

from stock.models import Stock, StockReview, StockReviewRecent60


def get_stock_type(stock_code):
    """判断股票ID对应的证券市场
    匹配规则
    ['50', '51', '60', '90', '110'] 为 sh
    ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    ['5', '6', '9'] 开头的为 sh， 其余为 sz
    :param stock_code:股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
    :return 'sh' or 'sz'"""
    assert type(stock_code) is str, "stock code need str type"
    sh_head = ("50", "51", "60", "90", "110", "113", "118",
               "132", "204", "5", "6", "9", "7")
    if stock_code.startswith(("sh", "sz", "zz")):
        return stock_code[:2]
    else:
        return "SH" if stock_code.startswith(sh_head) else "SZ"


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        x_day = datetime.datetime(2023, 3, 28, 15, 0, 0)
        st_reviews = StockReviewRecent60.objects.filter(createdAt=x_day).all()
        b_st_reviews = StockReviewRecent60.objects.filter(createdAt=x_day + datetime.timedelta(days=-1)).all()
        len1 = len(st_reviews)
        len2 = len(b_st_reviews)

        st_map = {}
        for st in b_st_reviews:
            st_map[st.code] = st


        all_st_reviews = []

        for c_st in st_reviews:
            old_st = st_map.get(c_st.code)
            if old_st:
                c_st.marketValue = old_st.marketValue
                c_st.tradingMarketValue = old_st.tradingMarketValue
                c_st.pe = old_st.pe
                c_st.turnoverRate = old_st.turnoverRate
                c_st.bid1Money = old_st.bid1Money
                all_st_reviews.append(c_st)

        bulk_update(all_st_reviews, update_fields=['marketValue', 'tradingMarketValue', 'pe', 'turnoverRate', 'bid1Money'])  # updates only name column


