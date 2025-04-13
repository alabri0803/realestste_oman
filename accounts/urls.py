from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
  path('login/', views.user_login, name='login'),
  path('register/', views.user_register, name='register'),
  path('logout/', views.user_logout, name='logout'),
  path('profile/', views.user_profile, name='profile'),
  path('change-password/', views.change_password, name='change_password'),
]