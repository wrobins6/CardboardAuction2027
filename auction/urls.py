from django.urls import path, include
from . import views

urlpatterns = [
    # -- debug only --	
    path('testpay_page', views.testpay_page, name='testpay_page'),
    path('testpay_action', views.testpay_action, name='testpay_action'),
    # -- general --
    path('home_page', views.home_page, name='home_page'),
    path('alter_page', views.alter_page, name='alter_page'),
    path('bid_action', views.bid_action, name='bid_action'),
    path('search_action', views.search_action, name='search_action'),
    path('error_page', views.error_page, name='error_page'),
    # -- consignment --
    path('consignment_page', views.consignment_page, name='consignment_page'),
    path('consignment_portal', views.consignment_portal, name='consignment_portal'),
    path('update_to_consigner', views.update_to_consigner, name='update_to_consigner'),
    path('consignment_action', views.consignment_action, name='consignment_action'),
]
