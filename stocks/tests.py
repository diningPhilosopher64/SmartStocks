from django.test import SimpleTestCase 
from django.urls import reverse, resolve
from .views import *


class TestUrls(SimpleTestCase):

    def test_list_url_resolves(self):
        url = reverse('stock_list')
        self.assertEquals(resolve(url).func.view_class, StockListView)

    def test_detail_url_resolves(self):
        url = reverse('stock_detail',args=['some_stock_name'])
        self.assertEquals(resolve(url).func.view_class, StockDetailView)

    def test_ChartData_url_resolves(self):
        url = reverse('chart_data')
        self.assertEquals(resolve(url).func.view_class, ChartData)


    def test_transaction_url_resolves(self):
        url = reverse('transaction',args=['some_stock_name'])
        self.assertEquals(resolve(url).func, transaction)

    def test_prediction_url_resolves(self):
        url = reverse('prediction_data')
        self.assertEquals(resolve(url).func.view_class, PredictionData)

    def test_Buy_url_resolves(self):
        url = reverse('buy_stock',args=['some_user','some_stock','some_quantity','some_stock'])
        self.assertEquals(resolve(url).func.view_class, BuyStock)

    def test_Sell_url_resolves(self):
        url = reverse('sell_stock',args=['some_user','some_stock','some_quantity','some_stock'])
        self.assertEquals(resolve(url).func.view_class, SellStock)