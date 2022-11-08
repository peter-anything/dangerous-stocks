import datetime

from django.core.management.base import BaseCommand

from stock.models import StockFundamental


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        all_stock_fundamentals = StockFundamental.objects.filter(
            turnoverRate__gte=20,
            createdAt__gte=datetime.datetime.now() + datetime.timedelta(days=-1))

        print(all_stock_fundamentals.count())
