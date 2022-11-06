import csv

import requests
from bs4 import BeautifulSoup, Tag


def get_all_stocks():
    with open('stock_detail.csv', 'w', encoding='utf-8', newline='\n') as f:
        csv_w = csv.writer(f)
        for page_num in range(1, 191):
            stock_list_url = 'https://vip.stock.finance.sina.com.cn/q/go.php/vFinanceAnalyze/kind/incomedetail/index.phtml?p=%d' % page_num
            resp = requests.get(stock_list_url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            table = soup.find_all(id='dataTable')[0]
            for table_content in table.contents:
                if isinstance(table_content, Tag):
                    if table_content.name == 'tr':
                        values = table_content.text.strip().split('\n')
                        csv_w.writerow(values)


if __name__ == '__main__':
    get_all_stocks()
