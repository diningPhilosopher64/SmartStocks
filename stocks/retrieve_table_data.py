from bs4 import BeautifulSoup
import requests


################### Handling Table data

def table_data(stock_name):
	base_url = "https://www.reuters.com/finance/stocks/companyProfile/"
	url = base_url + stock_name
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	table = soup.findAll("div", {"class": "column2"}) 

	return table[0]
