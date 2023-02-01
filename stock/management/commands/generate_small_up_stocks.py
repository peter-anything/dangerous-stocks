from datetime import datetime

from django.core.management.base import BaseCommand

from stock.models import StockReview


class BidStatistics(object):
    industry = ''
    count = 0
    total_close_money = 0
    stocks = []

    def __str__(self):
        return '''行业: %s，数量: %s, 包含股票: %s''' % (self.industry, self.count, '###'.join(['%s_%s_%s亿' % (stock['code'], stock['name'], stock['closeMoney']) for stock in self.stocks]))


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        now = datetime.now()
        stock = StockReview.objects.all()