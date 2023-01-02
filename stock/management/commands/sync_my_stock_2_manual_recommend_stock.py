from datetime import datetime

import easyquotation
from django.core.management.base import BaseCommand

from django.core.management.base import BaseCommand

from stock.models import MyStock, ManualRecommendStock


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        my_stocks = MyStock.objects.all()
        my_stock_codes = [stock.code for stock in my_stocks]
        manual_codes = [
            '600329',
            '000999',
            '600566',
            '603439',
            '603998',
            '002317',
            '002603',
            '603777',
            '605388',
            '603719',
            '001215',
            '600962',
            '002568',
            '600084',
            '000860',
            '603589',
            '000595',
            '002368',
            '300170',
            '603171',
            '603496',
            '603138',
            '000938',
            '300451',
            '301236',
            '002987',
            '300033',
            '600066',
            '000951',
            '002077',
            '300327',
            '600745',
            '603306',
            '603986',
            '600152',
            '601600',
            '000716',
            '000779',
            '000610',
            '000524',
            '605108',
            '002186',
            '301073',
            '300756',
            '601007',
            '002707',
            '603056',
            '002120',
            '002352',
        ]
        my_stock_codes.extend(manual_codes)
        stock_codes = set(my_stock_codes)
        quotation = easyquotation.use('tencent')
        print(len(stock_codes))
        now = datetime.now()
        #
        real_result = quotation.real([str(stock_code) for stock_code in stock_codes])
        for stock_code, detail in real_result.items():
            manual_recommend_stock = ManualRecommendStock()
            manual_recommend_stock.code = stock_code
            manual_recommend_stock.name = detail['name']
            manual_recommend_stock.save()
