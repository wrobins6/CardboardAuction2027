from django.urls import path, include
from . import views

urlpatterns = [

    path('login_page', views.login_page, name='login_page'),
    path('login_action', views.login_action, name='login_action'),
    
    path('register_page', views.register_page, name='register_page'),
    path('register_action', views.register_action, name='register_action'),
    
    path('login_success', views.login_success, name='login_success'),
    path('login_failure', views.login_failure, name='login_failure'),
    path('logout_action', views.logout_action, name='logout_action'),
    path('consignment_page', views.consignment_page, name='consignment_page'),
    path('consignment_portal', views.consignment_portal, name='consignment_portal'),
    path('update_to_consigner', views.update_to_consigner, name='update_to_consigner'),
    path('consignment_action', views.consignment_action, name='consignment_action'),
    
]
