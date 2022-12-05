import csv
import datetime

from django.core.management.base import BaseCommand

from django.core.management.base import BaseCommand

from stock.models import StockFundamental


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        f = open('testsql.txt', 'w', encoding='utf-8')
        all_stock_fundamentals = StockFundamental.objects.all()
        for stock_fundamental in all_stock_fundamentals:
            iclose = stock_fundamental.close
            iopen = stock_fundamental.open
            if iclose > 0 and iopen > 0:
                grothRate = (iclose - iopen) / iopen
                stock_fundamental.growthRate = grothRate * 100
                stock_fundamental.save()
            # if not stock_fundamental.close:
            #     continue
            # try:
            #     sql = '''
            #         INSERT INTO `stock_fundamental` (`code`, `name`, marketValue, tradingMarketValue, `open`, high, low, pe, turnoverRate, turnoverVolume, createdAt, `close`)  VALUES ('%s', '%s', %f, %f, %f, %f, %f, %f, NULL, NULL, '%s', %f);
            #     ''' % (
            #         stock_fundamental.code,
            #         stock_fundamental.name,
            #         stock_fundamental.marketValue,
            #         stock_fundamental.tradingMarketValue,
            #         stock_fundamental.open,
            #         stock_fundamental.high,
            #         stock_fundamental.low,
            #         stock_fundamental.pe,
            #         stock_fundamental.createdAt.strftime('%Y-%m-%d %H-%M-%S'),
            #         float(stock_fundamental.close)
            #     )
            #     f.write(sql +
            #             '\n')
            #     print(sql)
            # except:
            #     pass
        # code_map = {}
        # with open('2022-11-04.csv', 'r') as f:
        #     f_csv = csv.reader(f)
        #     for idx, row in enumerate(f_csv):
        #         if idx == 0: continue
        #         if not row: continue
        #         ts_code, trade_date, iopen, high, low, close, pre_close, change, pct_chg, vol, amount = row
        #         code_map[ts_code] = close
        #
        # all_stock_fundamentals = StockFundamental.objects.all()
        # now = datetime.datetime.now()
        # zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
        #                                       microseconds=now.microsecond)
        # for stock_fundamental in all_stock_fundamentals:
        #     try:
        #         StockFundamental.objects.filter(id=stock_fundamental.id).update(close=code_map[stock_fundamental.code],
        #                                                                         createdAt=zero_today + datetime.timedelta(-5) + datetime.timedelta(hours=15))
        #     except:
        #         pass
        # new_stock_fundamentals = []
        # code_map = {}
        # ids = []
        # for stock_fundamental in all_stock_fundamentals:
        #     if stock_fundamental.code in code_map:
        #         print(stock_fundamental.code)
        #         ids.append(stock_fundamental.id)
        #         continue
        #     code_map[stock_fundamental.code] = True
        #     new_stock_fundamentals.append(stock_fundamental)
        # print(len(new_stock_fundamentals))
        # StockFundamental.objects.filter(id__in=ids).delete()
