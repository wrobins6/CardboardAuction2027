from django.urls import path, include
from . import views

urlpatterns = [
    # -- debug only --	
    path('testpay_page', views.testpay_page, name='testpay_page'),
    path('testpay_action', views.testpay_action, name='testpay_action'),
    path('testship_page', views.testship_page, name='testship_page'),
    path('testship_action', views.testship_action, name='testship_action'),
    # -- general --
    path('home_page', views.home_page, name='home_page'),
    path('auction_page', views.auction_page, name='auction_page'),
    path('bid_action', views.bid_action, name='bid_action'),
    path('search_action', views.search_action, name='search_action'),
    path('error_page', views.error_page, name='error_page'),
    # -- consignment --
    path('consignment_page', views.consignment_page, name='consignment_page'),
    path('consignment_portal', views.consignment_portal, name='consignment_portal'),
    path('update_to_consigner', views.update_to_consigner, name='update_to_consigner'),
    path('consignment_action', views.consignment_action, name='consignment_action'),
    # -- curation --
    path('pending_alters', views.pending_alters, name='pending_alters'),
    path('works_under_management', views.works_under_management, name='works_under_management'),
    path('accept_pending_alter', views.accept_pending_alter, name='accept_pending_alter'),
    path('setup_auction_page', views.setup_auction_page, name='setup_auction_page'),
    path('setup_auction_action', views.setup_auction_action, name='setup_auction_action')
]
