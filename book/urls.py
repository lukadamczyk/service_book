from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'book'
urlpatterns = [
    path('', views.home, name='home'),
    path('vehicles/<slug>/', views.vehicle_list, name='vehicle_list'),
    path('vehicle/<slug>/', views.vehicle_detail, name='vehicle_detail'),
    path('complaint/', views.complaint_list, name='complaint_list'),
    path('complaint/<int:id>/', views.complaint_detail, name='complaint_detail'),
    path('complaint/edit/<int:id>/', views.edit_complaint, name='edit_complaint'),
    path('fault/<int:id>/', views.fault_detail, name='fault_detail'),
    path('complaint/add/', views.add_complaint, name='add_complaint'),
    path('fault/', views.fault_list, name='fault_list'),
    path('fault/edit/<int:id>/', views.edit_fault, name='edit_fault'),
    path('inspection/', views.inspection_list, name='inspection_list'),
    path('inspection/<int:id>/', views.inspection_detail, name='inspection_detail'),
    path('export/', views.export_complaints_xls, name='export_complaints_xls'),
    path('fault_without_complaint/<int:id>/', views.fault_without_complaint_detail,
         name='fault_without_complaint_detail'),
    path('fault_without_complaint/', views.fault_without_complaint_list, name='fault_without_complaint_list'),
    path('fault_without_complaint/add/', views.add_fault_without_complaint, name='add_fault_without_complaint'),
    path('fault_without_complaint/edit/<int:id>/', views.edit_fault_without_complaint,
         name='edit_fault_without_complaint'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)