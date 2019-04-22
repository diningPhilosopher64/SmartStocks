from django.urls import path
from .views import *
from . import views

urlpatterns = [
   

    path('', StockListView.as_view(), name='stock_list'),
    path('<str:stock_name>', StockDetailView.as_view(), name='stock_detail'),
    path('api/chart/data', ChartData.as_view(),name='chart_data'),
    path('api/prediction/data', PredictionData.as_view(),name='prediction_data'),
    path('transaction/<str:stock_name>',views.transaction, name='transaction'),
    path("api/buy/quantity/<str:current_user>/<str:stock_name>/<str:quantity>/<str:purchased_at>",BuyStock.as_view(),name = 'buy_stock'),
    path("api/sell/quantity/<str:current_user>/<str:stock_name>/<str:quantity>/<str:sold_at>",SellStock.as_view(), name = 'sell_stock'),





]
