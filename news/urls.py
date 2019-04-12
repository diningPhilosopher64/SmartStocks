from django.urls import path
from . import views
urlpatterns = [
    path('news/<str:stockSymbol>',views.stocknews,name='stocknews'),
    #path('',views.about,name='about'),
]