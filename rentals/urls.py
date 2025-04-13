from django.urls import path

from . import views

urlpatterns = [
  path('', views.home, name='home'),

  # الوحدات
  path('units/', views.units, name='units'),
  path('units/add/', views.add_unit, name='add_unit'),
  path('units/<int:pk>/', views.unit_detail, name='unit_detail'),
  path('units/<int:pk>/edit/', views.edit_unit, name='edit_unit'),

  # الشركات
  path('companies/', views.companies_list, name='companies_list'),
  path('companies/add/', views.add_company, name='add_company'),
  path('companies/<int:pk>/', views.company_detail, name='company_detail'),
  path('companies/<int:pk>/edit/', views.edit_company, name='edit_company'),

  # العقود
  path('contracts/', views.contracts_list, name='contracts_list'),
  path('contracts/add/', views.add_contract, name='add_contract'),
  path('contracts/<int:pk>/', views.contract_detail, name='contract_detail'),
  path('contracts/<int:pk>/edit/', views.edit_contract, name='edit_contract'),
  path('contracts/<int:pk>/renew/', views.renew_contract, name='renew_contract'),
  path('contracts/<int:pk>/terminate/', views.terminate_contract, name='terminate_contract'),

  # المدفوعات
  path('payments/', views.payments_list, name='payments_list'),
  path('payments/add/<int:contract_id>/', views.add_payment, name='add_payment'),

  # التقارير
  path('reports/', views.reports, name='reports'),
]