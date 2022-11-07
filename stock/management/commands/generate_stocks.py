import csv

from django.core.management.base import BaseCommand, CommandError

import easyquotation

from stock.models import Stock


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        code_set = set()

        stocks = []
        idx = 0
        with open('stock.csv', encoding='utf-8') as f:
            f_csv = csv.reader(f)
            for idx, line in enumerate(f_csv):
                if idx == 0:
                    continue
                if line[0] in code_set:
                    continue


                code_set.add(line[0])

                stock = Stock()
                stock.code = line[0]
                stock.name = line[1]
                stock.market = line[2]
                stock.category = line[3]
                stock.type = line[4]
                stocks.append(stock)

                idx += 1
                if idx % 1000 == 0:
                    Stock.objects.bulk_create(stocks)
                    stocks = []
        if len(stocks) > 0:
            Stock.objects.bulk_create(stocks)
