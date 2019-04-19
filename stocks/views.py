from django.shortcuts import render, get_object_or_404
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

from .models import Stock

from .ml import Preprocessing, Prediction
from .retrieve_table_data import table_data

from django.views.generic import (

    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    TemplateView
)


global current_stock




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
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        stock = Stock.objects.get(stock_name=current_stock)

        self.predict_price = Prediction(stock.stock_name).predict_stock_price()
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
    print("Curreent user is ",current_user)

    return render(request,"stocks/transaction.html")
