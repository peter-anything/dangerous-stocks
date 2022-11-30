import datetime

from django.core.management.base import BaseCommand
from django_bulk_update.helper import bulk_update

from stock.models import StockFundamental


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        all_stock_fundamentals = StockFundamental.objects.filter(
            createdAt__gte=datetime.datetime.now() + datetime.timedelta(days=-1))
        print(len(all_stock_fundamentals))
        for all_stock_fundamental in all_stock_fundamentals:
            print(all_stock_fundamental.id)
            print(all_stock_fundamental.code)
            print(all_stock_fundamental.name)
            if all_stock_fundamental.close > 0 and all_stock_fundamental.open > 0:
                print(all_stock_fundamental.close)
                print(all_stock_fundamental.open)
                all_stock_fundamental.growthRate = ((all_stock_fundamental.close - all_stock_fundamental.open) * 100 / all_stock_fundamental.open)
                print(all_stock_fundamental.growthRate)
        print(all_stock_fundamentals.count())
        bulk_update(all_stock_fundamentals, update_fields=['growthRate']) # updates only name column
