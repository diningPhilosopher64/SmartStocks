from iex import reference
from sqlalchemy import create_engine

company=reference.symbols()
company=company[['symbol','name']]
company['table_data']=""
company['description']=""
company['is_downloaded']=False
company.columns=['stock_name','company_name','table_data','description','is_downloaded']
user=input("Username for Postgres Database ?")
pwd=input("Enter Password :")
engine = create_engine('postgresql://'+user+':'+pwd+'@localhost:5432/smartstocksdb')
company.to_sql('stocks_stock', engine, if_exists='append', index=False)
print("Done!!!")


