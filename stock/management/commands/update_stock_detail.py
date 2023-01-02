import csv
import datetime
import json
from time import sleep

import requests
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from django_bulk_update.helper import bulk_update

from stock.models import Stock


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        stock_codes = []
        with open('all_stock_codes.txt', encoding='utf-8') as f:
            for line in f:
                values = line.split()
                code = values[0].strip()
                stock_codes.append(code)
                stock_codes = []
        stocks = Stock.objects.filter(market='A股').all()
        failed_codes = []
        print(len(stocks))
        with open('D:\\codes\\dangerous-stocks\\stock_detail_0102.csv', 'w', encoding='utf-8') as f:
            f_w = csv.writer(f)
            for stock_db in stocks:
                print(stock_db.code)
                try:
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36"}

                    stock_industry_url = 'https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpOtherInfo/stockid/{}/menu_num/5.phtml'.format(stock_db.code)
                    resp = requests.get(stock_industry_url, headers=headers)
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    div = soup.find_all(id='con02-0')[0]
                    tables = div.find_all('table')
                    industry_table = tables[0]
                    industry_td = industry_table.find_all('tr')[2].find_all('td')[0]
                    industry = industry_td.text.strip()
                    concept_table = tables[1]
                    concepts_tr = concept_table.find_all('tr')[2:]
                    all_concepts = []
                    for concept_tr in concepts_tr:
                        all_concepts.append(concept_tr.find_all('td')[0].text)

                    print(all_concepts)
                    print(industry)
                    stock_db.industry = industry
                    stock_db.concepts = json.dumps(all_concepts).encode().decode('unicode-escape')

                    stock_detail_url = 'https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/{}.phtml'.format(stock_db.code)
                    resp = requests.get(stock_detail_url, headers=headers)
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    div = soup.find_all(id='con02-0')[0]
                    tables = div.find_all('table')
                    detail_table = tables[0]
                    tds = detail_table.find_all('td')
                    marketingTime = tds[7].text.strip()
                    marketingPlace = tds[5].text.strip()
                    issuePrice = tds[9].text.strip()
                    underWriter = tds[11].text.strip()
                    regCapital = tds[15].text.strip()
                    regPlace = tds[43].text.strip()
                    regOfficePlace = tds[45].text.strip()
                    description = tds[47].text.strip()
                    mainBusiness = tds[49].text.strip()
                    establishTime = tds[13].text.strip()
                    print(marketingTime)
                    print(marketingPlace)
                    print(issuePrice)
                    print(underWriter)
                    print(regCapital)
                    print(regPlace)
                    print(regOfficePlace)
                    print(description)
                    print(mainBusiness)
                    print(establishTime)
                    stock_db.marketingTime = marketingTime
                    stock_db.marketingPlace = marketingPlace
                    stock_db.issuePrice = issuePrice
                    stock_db.underWriter = underWriter
                    stock_db.regCapital = regCapital
                    stock_db.regPlace = regPlace
                    stock_db.regOfficePlace = regOfficePlace
                    stock_db.description = description
                    stock_db.mainBusiness = mainBusiness
                    stock_db.establishTime = establishTime

                    row = [industry, json.dumps(all_concepts).encode().decode('unicode-escape'), marketingTime, marketingPlace, issuePrice, underWriter, regCapital, regPlace, regOfficePlace, description, mainBusiness, establishTime]
                    stock_db.save()
                    f_w.writerow(row)
                    sleep(0.5)
                except Exception as e:
                    print(e)
                    failed_codes.append(stock_db.code)
            print(failed_codes)
            # bulk_update(stocks) # updates only name column