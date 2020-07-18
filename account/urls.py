from django.urls import path, include

from account import views
from account.views import AccountCreate

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('create', AccountCreate.as_view(), name='account_create'),
]
