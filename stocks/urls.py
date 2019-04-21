from django.urls import path
from .views import *
from . import views

urlpatterns = [
   

    path('', StockListView.as_view(), name='stock_list'),
    path('<str:stock_name>', StockDetailView.as_view(), name='stock_detail'),
    #path('/chart/api/data/<slug:stock_name>',StockDetailView.as_view(),name='stock_detail'),
    #path('api/data',views.get_data, name='api-data'),
    path('api/chart/data', ChartData.as_view()),
    path('api/prediction/data', PredictionData.as_view()),
    path('transaction/<str:stock_name>',views.transaction, name='transaction'),
    path("api/buy/quantity/<str:current_user>/<str:stock_name>/<str:quantity>/<str:purchased_at>",BuyStock.as_view()),
    path("api/sell/quantity/<str:current_user>/<str:stock_name>/<str:quantity>/<str:sold_at>",SellStock.as_view()),





]
