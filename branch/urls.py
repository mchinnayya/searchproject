from django.urls import path
from branch import views
from branch.views import BranchCreate, BranchDetails, BranchList, BranchDelete

app_name = 'branch'
urlpatterns = [
    path('branch/create/', BranchCreate.as_view(), name='branch_create'),
    path('branch/update/<int:pk>/', views.branchupdate, name='branch_update'),
    path('branch/details/<int:pk>/',BranchDetails.as_view(), name='branch_details'),
    path('branch/list/', BranchList.as_view(), name='branch_list'),
    path('branch/delete/<int:pk>/',BranchDelete.as_view(), name='branch_delete'),
]
