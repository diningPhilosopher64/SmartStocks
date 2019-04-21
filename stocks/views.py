from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from keras import backend as K

import pandas as pd
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
import datetime
import time
import json
import urllib
import re
import requests
from bs4 import BeautifulSoup
import iex

# Stock Class in iex matches with Stock table in Db. Hence importing Stock_iex
from iex import Stock as Stock_iex
import decimal

from .models import Stock

from .ml import Preprocessing, Prediction
from .retrieve_table_data import table_data
from django.contrib.auth.models import User


from django.views.generic import (

    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    TemplateView
)
from accounts.models import Financials


global current_stock
global todays_prediction




# API endpoint for Chart, description and Table Data
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get_chart_data(self, stock):
        Data = None
        labels = None

        try:
            stock_file_name = stock.stock_name + ".csv"

            strFormat = "%Y-%m-%d"
            print("\n\n\n\n",os.getcwd(),"\n\n\n")
            df = pd.read_csv(os.path.join(os.getcwd(), "stocks_data", stock_file_name))
            date_parser = lambda word : datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(word),strFormat))).strftime("%d-%b-%Y")
            df['Date'] = df['Date'].map(date_parser)
            
            cols_to_delete = ['Open', 'High', 'Low', 'Adj Close', 'Volume']
            for col in cols_to_delete:
                del df[col]

            Data = list(df['Close'])
            labels = list(df['Date'])

        except:
            print("\n\n Chart Data Not Available \n\n")   


        return Data, labels

    def get_description(self, stock):

        try:
            url = "https://en.wikipedia.org/wiki/"+stock.company_name
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            self.table = soup.find_all("table", class_="infobox vcard")[0]

            #Get Description:
            session = requests.Session()
            URL = "https://en.wikipedia.org/w/api.php"
            SEARCHPAGE = stock.company_name
            PARAMS = {
                'action': "opensearch",
                'list': "search",
                'search': SEARCHPAGE,
                'format': "json"
            }

            response = session.get(url=URL, params=PARAMS)
            DATA = response.json()
            print("\n\n\n", DATA[2][0:2][0])
            return DATA[2][0:2]
        except:
            base_url = "https://www.reuters.com/finance/stocks/companyProfile/"
            url = base_url + stock.stock_name
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            mydivs = soup.findAll("div", {"class": "moduleBody"})
            data = mydivs[1].findChildren("p")[0].text

            return data



    def get_table_data(self, stock):
        url = "https://en.wikipedia.org/wiki/"

        table = None

        try:
            full_path = url +  stock.company_name
            page = requests.get(full_path)
            soup = BeautifulSoup(page.text, 'html.parser')        
            table = soup.find_all("table", class_="infobox vcard")[0]
        except:
            base_url = "https://www.reuters.com/finance/stocks/companyProfile/"
            company_url = base_url + stock.stock_name
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            table = soup.findAll("div", {"class": "column2"})

            if not table:
                table = table_data(stock.stock_name)



        return table

    def get(self, request, format=None):

        stock = Stock.objects.get(stock_name=current_stock)

        # Get data from csv to chart them.
        Data, labels = self.get_chart_data(stock)

        self.table = None
        self.description = None

        if stock.is_downloaded == True:
            self.table = stock.table_data
            self.description = stock.description

        else:
            self.table = self.get_table_data(stock)
            self.description = self.get_description(stock)

            #Updating the stock Object
            stock.is_downloaded = True
            stock.company_name
            stock.table_data = str(self.table)
            stock.description = self.description
            stock.save()
        

        
        data = {
            "table_data": str(self.table),
            "labels": labels,
            "Data": Data,
            "Description": self.description,
        }

        return Response(data)


class PredictionData(APIView):
    global todays_prediction 
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        stock = Stock.objects.get(stock_name=current_stock)

        self.predict_price = Prediction(stock.stock_name).predict_stock_price()
        todays_prediction = self.predict_price
        K.clear_session()

        context = {
            "prediction": self.predict_price,
        }


        return Response(context)





class StockListView(ListView):
    template_name = "stocks/stock_list.html"
    queryset = Stock.objects.all()


class StockDetailView(DetailView):
    template_name = "stocks/stock_detail.html"

    def get_object(self):
        global current_stock
        stock_name = self.kwargs.get('stock_name')
        current_stock = stock_name
        return get_object_or_404(Stock, stock_name=stock_name)





def transaction(request,stock_name):
    

    current_user = request.user
    user_financials = Financials.objects.get(user = current_user)
    columns = ['cashFlow','currentAssets','operatingIncome','grossProfit','totalLiabilities','totalRevenue']


    stock = iex.Stock(stock_name)
    company_name = stock.company()['companyName']
    todays_price = stock.price() 
    effective_spread_html = stock.effective_spread_table()[:4].to_html()
    financials_table =stock.financials_table()
    financials_table_html = financials_table[columns].to_html()

    stocks_owned = user_financials.stocks_owned

    buy = True
    if user_financials.balance < todays_price:
        buy = False


    context = {
        "user_financials": user_financials,
        "user": current_user,
        "effective_spread": effective_spread_html,
        "todays_price": todays_price,
        "company_name": company_name,
        "financials": financials_table_html,
        "user_financials": user_financials,
        "buy": buy,
        "stock_name":stock_name,        
        
    }   

    sell = False
    if not stocks_owned:
        context['sell'] = sell
        return render(request,"stocks/transaction.html",context)


    stocks_owned = eval(stocks_owned)
    for item in stocks_owned:
        if item['stock_name'] == stock_name:
            sell = True
            context['sell'] = sell
            break

    return render(request,"stocks/transaction.html",context)





        

class BuyStock(APIView):
    authentication_classes = []
    permission_classes = []
    

    def stocks_packer(self,stocks_owned,stock_name,quantity,purchased_at,buying):    
        current_stock= {}
        current_stock["stock_name"] = stock_name
        current_stock["quantity"] = quantity
        current_stock['purchased_at'] = purchased_at

        if not stocks_owned:
            stocks_owned = []
            stocks_owned.append(current_stock);
            return stocks_owned
        
        else:
            
            stocks_owned = eval(stocks_owned)               
            for stock in stocks_owned:
                if stock['stock_name'] == stock_name:
                    stock['quantity'] += int(quantity)
                    stock['purchased_at'] = purchased_at
                    return stocks_owned               
            


            stocks_owned.append(current_stock)
            return stocks_owned 




    def post(self, request,current_user,stock_name,quantity,purchased_at, format=None):
                
        user_financials = Financials.objects.get(user = current_user)

        quantity = int(quantity)
        purchased_at = float(purchased_at)

        stocks_owned = user_financials.stocks_owned
        buying = True
        stocks_owned = self.stocks_packer(stocks_owned,stock_name,quantity,purchased_at,buying)
        balance = user_financials.balance

        context = {
            "updated_balance": balance,
            "message": "Insufficient Funds..!"           
        }

        if quantity * purchased_at > balance:
            return Response(context)
    
        balance -= decimal.Decimal(quantity * purchased_at)

        user_financials.balance =  balance 
        user_financials.stocks_owned = str(stocks_owned)
        user_financials.save()  

        print("stocks_owned",user_financials.stocks_owned)     


        context['updated_balance'] = balance
        context['message'] = "Stock Purchased ! \n Balance Updated."
        return Response(context)



class SellStock(APIView):
    authentication_classes = []
    permission_classes = []          

    def can_sell(self,stocks_owned,stock_name,quantity):
        sellable = False
        index = -1
        for stock in stocks_owned:
            index += 1
            if stock['stock_name'] == stock_name:
                if stock['quantity'] > quantity:
                    sellable = True
                    break
        return sellable,index
                      


    def post(self, request,current_user,stock_name,quantity,sold_at, format=None):
                
        user_financials = Financials.objects.get(user = current_user)

        quantity = int(quantity)
        purchased_at = float(sold_at)
        balance = user_financials.balance
        stocks_owned = eval(user_financials.stocks_owned)
        context = {
            "updated_balance": balance,
            "message": "Cant sell more than you own."           
        }


        sellable,index = self.can_sell(stocks_owned,stock_name,quantity)
        if not sellable:
            return Response(context)

        else:                        
        
            balance += decimal.Decimal(quantity * purchased_at)
            stocks_owned[index]['quantity'] -= quantity


            user_financials.balance =  balance 
            user_financials.stocks_owned = str(stocks_owned)
            user_financials.save()  

            context['updated_balance'] = balance
            context["message"] = "Sold Stock Successfully..! Balance Updated."
            
            return Response(context)
