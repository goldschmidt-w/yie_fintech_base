
import time
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import sqlalchemy


def get_stock_id():
	"""
	get stock_ids from industry webpage
	可以參考 廖敏煌 的方法
	demands:


	process:
	(1)import request
	(2)import pandas as pd
	(3)pd.read_html
	"""


def update_stock_id():
	"""
	update stosck_id in  stock_ids table
	demands：

	process:
	(1)read in stock_ids from stock_ids table
	(2)add stock_id if stock_id NOT in stock_ids

	"""


def generate_urls(the_base_url, stock_ids, *arg):
	"""
	generate the specific urls:
	demands:
	(1) trade stock_id, status, spohlcv
	    stock_id, price, open(yclose), high, low, close, volume
	    https://tw.stock.yahoo.com/quote/8926.TW

	(2) IFRS seasonly reports
		https://mops.twse.com.tw/server-java/t164sb01?step=1\
		&CO_ID=8926&SYEAR=2021&SSEASON=4&REPORT_ID=C

	process:
	(1) integrate the_base_url and the specific url_parameters

	"""
	urls = []
	for stock_id in stock_ids:
		urls.append(the_base_url + stock_id)
	return urls


def get_resource(urls):
	
	header = {} # need append the specific server response headers
	return requests.get(urls, headers=headers)


def parse_static_html(html_str):

	return bs(html_str, 'lxml')


def strainer_stock_spohlcv(bs_dom, stock_id):
	"""
	continued from parse_static_html(), 
	retrieve pohlcv from the "https://tw.stock.yahoo.com/quote/8926.TW"
	response.

	?close


	"""
	table = bs_dom.find_all(text='成交')[0].parent.parent.parent
	status = table.select('tr')[0].select('th')[2].text
	name = table.select('tr')[1].select('td')[0].text
	price = table.select('tr')[1].select('td')[2].text
	yclose = table.select('tr')[1].select('td')[7].text	
	high = table.select('tr')[1].select('td')[9].text
	low = table.select('tr')[1].select('td')[10].text
	volume = table.select('tr')[1].select('td')[6].text

	return [stock_id, name[4:-6], status, price, yclose, high, low, volume]


def stock_spohlcv_bot(urls):
	"""
	strainer_stock_spohlcv provides spohlcv from a fixed table
	Herein, "zipped" spohlcv, sinnce s(stock_id is trigger)
	demand:
	
	process:
	calling functions above to generate spohlcv

	"""

	stock_ids_spohlv = [['代碼', '名稱', '狀態', '股價', '昨收', '最高', '最低', '張數']]
	#                  stock_id, name, status, price, yclose, hight, low, volume
	for url in urls:
		response = get_resource(url)
		if response.status_code == requests.codes.ok:
			bs_dom = parse_static_html(response.text)
			stock_ids_spohlv_result = get_stock_spohlcv(bs_dom, stock_id)
			stock_ids_spohlv.append(stock_ids_spohlv_result)
			time.sleep(0.25)
		else:
			print('HTTP response error...')
	return stock_ids_spohlv


def update_spohlcv_tosql(stock_id):
	"""

	"""


def strainer_balance_sheet(bs_dom, stock_id, year, searon, *arg):
	"""
	IFRS_balance_keys = {'3200': '資本公積合計',
						 '3300': '保留盈餘合計',
						 '3500': '庫藏股票',
						 }

	"""


def update_balance_tosql(stock_id):
	"""
	
	"""


def strainer_revenue_sheet(bs_dom, stock_id, year, seaon, *arg):
	"""
	IFRS_revenue_keys = {'4000': '營業收入合計', 
						'7000: '營業外收入及支出合計',
						'8200': '本期淨利（淨損）',
						'8300': '其他綜合損益（淨額）',
						'9750': '基本每股盈餘合計',
						'9850': '稀釋每股盈餘合計',
						}

	"""


def update_revenue_tosql(stock_id):
	"""
	
	"""


def strainer_external_invest(bs_dom, stock_id, year, season, *arg):
	"""


	"""


def update_external_invest_tosql(stock_id):
	"""
	
	"""


def strainer_chn_invest(bs_dom, stock_id, year, season, *arg):
	"""

	"""


def update_chn_invest_tosql(stock_id):
	"""
	
	"""


def main():
	the_base_url = ''
	stock_ids = []
	urls = generate_urls(the_base_url, stock_ids)
	stock_ids_spohlv = stock_spohlcv_bot(urls)
	for stock in stock_ids_spohlv:
		print(stock)


if __name__ == '__main__':
	main()