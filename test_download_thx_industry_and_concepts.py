import csv

import requests
from bs4 import BeautifulSoup, Tag

REQ_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}


def get_industry_detail(industry_detail_url):
    resp = requests.get(industry_detail_url, headers=REQ_HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    heading_bref = soup.find_all(attrs={"class": "board-hq"})
    heading_detail = soup.find_all(attrs={"class": "board-infos"})[0]
    dls = heading_detail.find_all('dl')
    industry_detail = {}
    for dl in dls:
        dt = dl.find_all('dt')[0]
        dd = dl.find_all('dd')[0]
        name = dt.text
        value = dd.text
        industry_detail[name] = value

    print(industry_detail)


def get_all_industries():
    industry_url = 'http://q.10jqka.com.cn/thshy/'
    resp = requests.get(industry_url, headers=REQ_HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    cate_groups = soup.find_all(attrs={"class": "cate_group"})
    for cate_group in cate_groups:
        cate_items = cate_group.find_all("a")
        for cate_item in cate_items:
            industry_detail_url = cate_item.attrs['href']
            industry_name = cate_item.text
            get_industry_detail(industry_detail_url)
            print(cate_item)
    print(soup)


def get_all_concepts():
    industry_url = 'http://q.10jqka.com.cn/gn/'


if __name__ == '__main__':
    get_all_industries()
