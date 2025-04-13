from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
  path('', views.payment_list, name='payment_list'),
  path('payments/<int:pk>/', views.payment_detail, name='payment_detail'),
  path('add/<int:contract_id>/', views.payment_create, name='payment_create'),
  path('<int:pk>/edit/', views.payment_update, name='payment_update'),
  path('<int:pk>/delete/', views.payment_delete, name='payment_delete'),
  path('invoice/generate/<int:pk>/', views.generate_invoice, name='generate_invoice'),
  path('invoice/download/<int:pk>/', views.download_invoice, name='download_invoice'),
]