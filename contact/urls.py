from django.urls import path
from contact import views
from contact.views import EmergencyDetailsDelete, EmergencyDetailsDetails, EmergencyDetailsList
app_name = 'emergency'
urlpatterns = [
    path('emergency/delete/<int:pk>/',EmergencyDetailsDelete.as_view(), name='emergencyDetails_delete'),
    path('emergency/create/', views.EmergencyDetailsCreate.as_view(),name='emergencyDetails_create'),
    path('emergency/details/<int:pk>/',EmergencyDetailsDetails.as_view(), name='emergencyDetails_details'),
    path('', EmergencyDetailsList.as_view(), name='emergencyDetails_list'),
    path('emergency/update/<int:pk>/',views.emergency_detailsupdate, name='emeregcy_update'),
    path('emergency/make-it-active/<int:pk>/',views.emeregcy_active, name='emeregcy_active'),
    path('emergency_csv_upload/', views.emergency_upload, name='emergency_upload'),
    path('emergency-details-search/',views.emergency_details_search, name='emergency_details_search'),
    path('favorite_save', views.favorite_save, name='favorite_save'),
    path('favorite_contact_save', views.favorite_contact_save,name='favorite_contact_save'),
]
