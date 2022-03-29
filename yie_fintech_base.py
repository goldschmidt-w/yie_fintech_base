
import time
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import sqlalchemy


def get_stock_id():
	"""
	get stock_ids from 產業分表
	可以參考 廖敏煌 的方法
	demands:

	process:
	import request
	import pandas as pd
	pd.read_html
	"""


def update_stock_id():
	"""
	update stosck id in  stock_ids table
	demands：

	process:
	(1)read in stock_ids from stock_ids table
	(2)add stock_id if stock_id NOT in stock_ids

	"""

def generate_urls(the_base_url, stock_ids):
	
	urls = []
	for stock_id in stock_ids:
		urls.append(the_base_url + stock_id)
	return urls


def get_resource(urls):
	
	header = {} # need append the specific server response headers
	return requests.get(urls, headers=headers)


def parse_html(html_str):

	return bs(html_str, 'lxml')


def get_stock_spohlcv(bs_dom, stock_id):

	table = bs_dom.find_all(text='成交')[0].parent.parent.parent
	status = table.select('tr')[0].select('th')[2].text
	name = table.select('tr')[1].select('td')[0].text
	price = table.select('tr')[1].select('td')[2].text
	yclose = table.select('tr')[1].select('td')[7].text	
	high = table.select('tr')[1].select('td')[9].text
	low = table.select('tr')[1].select('td')[10].text
	volume = table.select('tr')[1].select('td')[6].text

	return [stock_id, name[4:-6], status, price, yclose, high, low, volume]


def web_scrape_bot(urls):

	stock_ids_spohlv = [['代碼', '名稱', '狀態', '股價', '昨收', '最高', '最低', '張數']]
	#                  stock_id, name, status, price, yclose, hight, low, volume
	for url in urls:
		response = get_resource(url)
		if response.status_code == requests.codes.ok:
			bs_dom = parse_html(response.text)
			stock_ids_spohlv_result = get_stock_spohlcv(bs_dom, stock_id)
			stock_ids_spohlv.append(stock_ids_spohlv_result)
			time.sleep(0.25)
		else:
			print('HTTP response error...')
	return stock_ids_spohlv


def main():
	the_base_url = ''
	stock_ids = []
	urls = generate_urls(the_base_url, stock_ids)
	stock_ids_spohlv = web_scrape_bot(urls)
	for stock in stock_ids_spohlv:
		print(stock)

if __name__ == '__main__':
	main()