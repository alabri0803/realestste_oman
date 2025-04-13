from django.urls import path

from . import views

app_name = 'companies'

urlpatterns = [
  path('', views.CompanyListView.as_view(), name='company_list'),
  path('<int:pk>/', views.company_detail, name='company_detail'),
  path('add/', views.company_create, name='company_create'),
  path('<int:pk>/edit/', views.company_update, name='company_update'),
  path('<int:pk>/delete/', views.company_delete, name='company_delete'),
]