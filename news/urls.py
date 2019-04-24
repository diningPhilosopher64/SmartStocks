from django.urls import path
from . import views
urlpatterns = [
    path('news/<str:stockSymbol>',views.stocknews,name='stocknews'),
    path('news/all',views.all_news,name='all_news'),

]