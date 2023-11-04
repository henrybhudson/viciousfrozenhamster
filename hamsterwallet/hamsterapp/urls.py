from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_page,name='login'),
    path('home/',views.process_login_request,name='loginsubmit'),
    path('register/',views.register_page,name='registersite'),
    path('signup/',views.process_register_request,name='registersubmit'),
    path('transaction/',views.add_transaction,name='addtransaction')
]