from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.home, name='home'),
    path('vehicles/<slug>/', views.vehicle_list, name='vehicle_list'),
    path('vehicle/<slug>/', views.vehicle_detail, name='vehicle_detail'),
    path('complaint/', views.complaint_list, name='complaint_list'),
    path('complaint/<int:id>/', views.complaint_detail, name='complaint_detail'),
    path('fault/<int:id>/', views.fault_detail, name='fault_detail'),
    path('complaint/add/', views.add_complaint, name='add_complaint'),
    path('fault/', views.fault_list, name='fault_list'),
    path('inspection/', views.inspection_list, name='inspection_list'),
    path('inspection/<int:id>/', views.inspection_detail, name='inspection_detail'),
    path('export/', views.export_complaints_xls, name='export_complaints_xls'),
]