import datetime

from django.core.management.base import BaseCommand
from django_bulk_update.helper import bulk_update

from stock.models import StockFundamental


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        stock_fundamentals = StockFundamental.objects\
            .filter(growthRate__gte=5)

        print(stock_fundamentals.count())