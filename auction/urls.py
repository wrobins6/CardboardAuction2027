from django.urls import path, include
from . import views

urlpatterns = [
    path('testpay_page', views.testpay_page, name='testpay_page'),
    path('testpay_action', views.testpay_action, name='testpay_action'),
    path('home_page', views.home_page, name='home_page'),
    path('alter_page', views.alter_page, name='alter_page'),
    path('bid_action', views.bid_action, name='bid_action'),
    path('search_action', views.search_action, name='search_action')
]
