from datetime import datetime, timedelta
from time import sleep

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from stock.models import IndustryBlock, ConceptBlock

REQ_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

now = datetime.now()

zero_today = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                             microseconds=now.microsecond)


def get_industry_detail(industry_detail_url):
    resp = requests.get(industry_detail_url, headers=REQ_HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    heading_brief = soup.find_all(attrs={"class": "board-xj"})[0]
    heading_detail = soup.find_all(attrs={"class": "board-infos"})[0]
    dls = heading_detail.find_all('dl')
    industry_detail = {
        'now': heading_brief.text.strip()
    }
    for dl in dls:
        dt = dl.find_all('dt')[0]
        dd = dl.find_all('dd')[0]
        name = dt.text
        value = dd.text
        industry_detail[name] = value

    return industry_detail


def get_all_industries():
    industry_url = 'http://q.10jqka.com.cn/thshy/'
    resp = requests.get(industry_url, headers=REQ_HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    cate_groups = soup.find_all(attrs={"class": "cate_group"})
    industry_blocks = IndustryBlock.objects.filter(createdAt__gt=zero_today).all()
    industry_block_map = {}
    for ib in industry_blocks:
        industry_block_map[ib.code] = True

    industry_block_arr = []
    for cate_group in cate_groups:
        cate_items = cate_group.find_all("a")
        for cate_item in cate_items:
            industry_detail_url = cate_item.attrs['href']
            industry_name = cate_item.text
            industry_code = industry_detail_url.split('/')[-2]
            if industry_code in industry_block_map:
                continue
            industry_detail = get_industry_detail(industry_detail_url)
            industry_block = IndustryBlock()
            industry_block.code = industry_code
            industry_block.name = industry_name
            industry_block.now = industry_detail['now']
            industry_block.open = industry_detail['今开']
            industry_block.close = industry_detail['昨收']
            industry_block.high = industry_detail['最高']
            industry_block.low = industry_detail['最低']
            industry_block.volume = industry_detail['成交量(万手)']
            up_count, down_count = industry_detail['涨跌家数'].strip().split('\n')
            industry_block.upCount = up_count
            industry_block.downCount = down_count
            industry_block.inFlowFunds = industry_detail['资金净流入(亿)']
            industry_block.turnover = industry_detail['成交额(亿)']
            industry_block.growthRate = industry_detail['板块涨幅'][:-1]
            industry_block_arr.append(industry_block)
            industry_block.createdAt = zero_today + timedelta(hours=15)
            industry_block.save()

            # sleep(1)

    # IndustryBlock.objects.bulk_create(industry_block_arr)


def get_all_concepts():
    industry_url = 'http://q.10jqka.com.cn/gn/'
    resp = requests.get(industry_url, headers=REQ_HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    cate_groups = soup.find_all(attrs={"class": "cate_group"})
    industry_blocks = IndustryBlock.objects.filter(createdAt__gt=zero_today).all()
    industry_block_map = {}
    for ib in industry_blocks:
        industry_block_map[ib.code] = True

    industry_block_arr = []
    for cate_group in cate_groups:
        cate_items = cate_group.find_all("a")
        for cate_item in cate_items:
            try:
                industry_detail_url = cate_item.attrs['href']
                industry_name = cate_item.text
                industry_code = industry_detail_url.split('/')[-2]
                if industry_code in industry_block_map:
                    continue
                industry_detail = get_industry_detail(industry_detail_url)
                industry_block = ConceptBlock()
                industry_block.code = industry_code
                industry_block.name = industry_name
                industry_block.now = industry_detail['now']
                industry_block.open = industry_detail['今开']
                industry_block.close = industry_detail['昨收']
                industry_block.high = industry_detail['最高']
                industry_block.low = industry_detail['最低']
                industry_block.volume = industry_detail['成交量(万手)']
                up_count, down_count = industry_detail['涨跌家数'].strip().split('\n')
                industry_block.upCount = up_count
                industry_block.downCount = down_count
                industry_block.inFlowFunds = industry_detail['资金净流入(亿)']
                industry_block.turnover = industry_detail['成交额(亿)']
                industry_block.growthRate = industry_detail['板块涨幅'][:-1]
                industry_block_arr.append(industry_block)
                industry_block.createdAt = zero_today + timedelta(hours=15)
                industry_block.save()
            except:
                print(industry_detail_url)
                pass

            # sleep(1)


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        # industries = get_all_industries()
        concepts = get_all_concepts()
