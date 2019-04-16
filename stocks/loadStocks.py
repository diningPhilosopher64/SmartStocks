from iex import reference
from sqlalchemy import create_engine
import os

cwd = os.getcwd().split("/")[:-1]
path = ("/").join(cwd)
path = os.path.join(path,"stocks_data")
available_stocks = os.listdir(path)
available_stocks = [stock[:-4]for stock in available_stocks]

company=reference.symbols()
company=company[['symbol','name']]
company['table_data']=""
company['description']=""
company['is_downloaded']=False
company.columns=['stock_name','company_name','table_data','description','is_downloaded']
company=company[company['stock_name'].isin(available_stocks)]

user=input("Username for Postgres Database ?")
pwd=input("Enter Password :")
engine = create_engine('postgresql://'+user+':'+pwd+'@localhost:5432/smartstocksdb')
company.to_sql('stocks_stock', engine, if_exists='append', index=False)
print("Done!!!")


