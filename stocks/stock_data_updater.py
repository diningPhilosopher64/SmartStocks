import os
import subprocess
import time

from datetime import date,timedelta
from time import mktime
from iex import Stock, reference
from iexfinance.stocks import get_historical_data
from datetime import datetime
from time import sleep
import pandas as pd
import os
import iex
import csv


from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
yf.pdr_override()


cwd = os.getcwd().split("/")[:-1]
path = ("/").join(cwd)
path = os.path.join(path,"stocks_data")
available_stocks = os.listdir(path)

available_stocks = [stock[:-4]for stock in available_stocks]

available_stocks.sort()


def get_file_path(symbol):
    cwd = os.getcwd().split("/")[:-1]
    path = ("/").join(cwd)
    file_path = os.path.join(path,"stocks_data",symbol+".csv")
    return "".join(file_path)


for i in range(0,len(available_stocks)):
    
   
    current_symbol = available_stocks[i]
    today = datetime.today().date()
        
    try:
        sleep(1)
        current_stock =  Stock(current_symbol)
        price = current_stock.price()
        row = [str(today),0,0,0]
#         row.append(str(today))
#         row.append(0)
        row.append(price)
        row.append(0)
        row.append(0)    
        file_path = get_file_path(current_symbol)
        
        print("Updating stock : ",current_symbol)
		        
    except:
        print("Error")
        i -= 1
        sleep(3)
        
        
    with open(file_path,'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)      
