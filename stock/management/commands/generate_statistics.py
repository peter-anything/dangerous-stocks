import datetime

import easyquotation
from django.core.management.base import BaseCommand

from stock.models import Stock, StockReview


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        now = datetime.datetime.now()

        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond)

        stock_reviews = StockReview.objects.filter(createdAt__gt=zero_today) \
            .order_by('code', '-id') \
            .exclude(code__istartswith='30') \
            .exclude(code__istartswith='688') \
            .exclude(name__startswith='*ST') \
            .exclude(marketValue__lt=40) \
            .all()
        stock_statistics = {
            'bigUp': [],  # 5
            'smallUp': [],  # 2.9-5
            'up': [],  # 1.9 - 2.9
            'upDown': [],  # -1.9 ~ 1.9
            'down': [],  # -3 ~ -2
            'smallDown': [],  # -5 ~ -3,
            'bigDown': [],  # -5,
        }
