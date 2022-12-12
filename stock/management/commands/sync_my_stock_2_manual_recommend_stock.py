from datetime import datetime

import easyquotation
from django.core.management.base import BaseCommand

from django.core.management.base import BaseCommand

from stock.models import MyStock, ManualRecommendStock


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        stocks = MyStock.objects.all()
        stock_codes = [stock.code for stock in stocks]
        quotation = easyquotation.use('tencent')
        now = datetime.now()
        manual_recommend_stocks = ManualRecommendStock.objects.all()
        manual_recommend_stock_codes = [stock.code for stock in manual_recommend_stocks]
        stock_codes = set(stock_codes) - set(manual_recommend_stock_codes)

        real_result = quotation.real([str(stock_code) for stock_code in stock_codes])
        for stock_code, detail in real_result.items():
            manual_recommend_stock = ManualRecommendStock()
            manual_recommend_stock.code = stock_code
            manual_recommend_stock.name = detail['name']
            manual_recommend_stock.save()
