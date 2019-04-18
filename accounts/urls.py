from django.urls import path
from . import views

urlpatterns = [

    path('',views.index,name ='index'),   
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('all_users', views.all_users, name='all_users'),
    path('user_details/<str:username>', views.user_details, name='user_details'),
    path('edit/<str:username>', views.edit, name='edit'),    

]
