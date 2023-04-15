from django.core.management.base import BaseCommand
from django.db import connection


import pymysql

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     port=13986,
                     user='root',
                     password='abc123_',
                     database='smart_stocks')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()



class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        with open('/Users/wangxiaobin/Downloads/stock_fundamental1.sql', encoding='utf-8') as f:
            with connection.cursor() as cursor:
                sqls = []
                for sql in f:
                    sqls.append(sql[sql.index('VALUES') + 6:-2].strip())

                    if len(sqls) % 1000 == 0:
                        real_sql = '''INSERT INTO `stock_fundamental` (`id`, `code`, `name`, `marketValue`, `tradingMarketValue`, `open`, `high`, `low`, `close`, `pe`, `turnoverRate`, `turnoverVolume`, `tradingMoney`, `createdAt`, `growthRate`) values %s ''' % ','.join(sqls)
                        # print(real_sql)
                        # cursor.execute(real_sql)
                        sqls = []
                if len(sqls) > 0:
                    real_sql = '''INSERT INTO `stock_fundamental` (`id`, `code`, `name`, `marketValue`, `tradingMarketValue`, `open`, `high`, `low`, `close`, `pe`, `turnoverRate`, `turnoverVolume`, `tradingMoney`, `createdAt`, `growthRate`) values %s ''' % ','.join(sqls)
                    print(real_sql)
                    cursor.execute(real_sql)
