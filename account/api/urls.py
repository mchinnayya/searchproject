from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from account.api import views

urlpatterns = [
    path('', views.account_list, name="account_api_list"),
]
urlpatterns = format_suffix_patterns(urlpatterns)