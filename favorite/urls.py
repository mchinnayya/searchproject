from django.urls import path

from favorite import views
from common.context_processors import get_favorite_list,favorite_form

app_name = 'favorite'
urlpatterns = [
    path('fav_contact_create', views.Favorite_Contact_Create.as_view(), name='favorite_contact_create'),
    path('favorite/<int:id>/', views.FavoriteDetails.as_view(), name='favorite_contact_view'),
]
