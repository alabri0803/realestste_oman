from django.urls import path

from . import views

app_name = 'rentals'

urlpatterns = [
  # المباني
  path('buildings/', views.BuildingListView.as_view(), name='building_list'),
  path('buildings/<int:pk>/', views.building_detail, name='building_detail'),
  path('buildings/add/', views.building_create, name='building_create'),
  path('buildings/<int:pk>/edit/', views.building_update, name='building_update'),
  path('buildings/<int:pk>/delete/', views.building_delete, name='building_delete'),

  # الوحدات
  path('units/', views.unit_list, name='unit_list'),
  path('units/<int:pk>/', views.unit_detail, name='unit_detail'),
  path('units/add/', views.unit_create, name='unit_create'),
  path('units/<int:pk>/edit/', views.unit_update, name='unit_update'),
  path('units/<int:pk>/delete/', views.unit_delete, name='unit_delete'),

  # العقود
  path('contracts/', views.contract_list, name='contract_list'),
  path('contracts/<int:pk>/', views.contract_detail, name='contract_detail'),
  path('contracts/add/', views.contract_create, name='contract_create'),
  path('contracts/<int:pk>/edit/', views.contract_update, name='contract_update'),
  path('contracts/<int:pk>/renew/', views.contract_renew, name='contract_renew'),
  path('contracts/<int:pk>/terminate/', views.contract_terminate, name='contract_terminate'),

  # الرئيسية
  path('', views.home, name='home')
]