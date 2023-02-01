import datetime
import json

from django.core.management.base import BaseCommand

from stock.models import StockFundamental, Stock


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        concept_map = {
            '人工智能': ['人工智能'],
            '军工': ['国防军工', '军工电子', '航天军工', '航天航空', '航天科工集团', '航空工业集团', '军工航天'],
            '稀土和有色': ['小金属', '稀土永磁', '有色铝', '有色锌'],
            '网安': ['网络安全', '安全'],
            '国资云': ['云服务'],
            '数字经济': ['数字经济'],
            '信创': ['信创'],
            '中字头': ['中字头'],
            'TOPCon': ['TOPCon电池', 'TOPCon'],
            'HJT电池': ['HJT电池'],
            '工业母机': ['工业母机'],
            '储能': ['储能'],
            '动力煤': ['动力煤'],
            '航天航空': ['航天军工', '航天航空', '航天科工集团', '航空工业集团', '军工航天'],
            '新基建': ['新基建'],
            '种业': ['种业'],
            '家用电器': ['家用电器', '智能家居'],
            '机器人': ['智能机器']
        }
        all_stocks = Stock.objects \
            .exclude(code__istartswith='300').exclude(code__istartswith='688').exclude(name__startswith='ST') \
            .exclude(name__startswith='*ST') \
            .filter(market='A股')

        concepts_map = {}
        for st in all_stocks:
            if st.concepts:
                concepts = json.loads(st.concepts)
                for c in concepts:
                    concepts_map[c] = None

        print(concepts_map.keys())

