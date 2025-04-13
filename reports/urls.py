from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
  path('financial/', views.financial_report, name='financial_report'),
  path('occupancy/', views.occupancy_report, name='occupancy_report'),
  path('export/', views.export_data, name='export_data'),
]