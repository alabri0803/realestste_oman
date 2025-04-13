from django.urls import path
from django.views.i18n import set_language

from . import views
from .views import (
  CompanyDocumentCreateView,
  CustomLoginView,
  PasswordChangeRTLView,
  ProfileUpdateView,
  SignUpView,
)

urlpatterns = [
  # مصادقة المستخدمين
  path('login/', CustomLoginView.as_view(), name='login'),
  path('logout/', views.CustomLogoutView.as_view(), name='logout'),

  # إدارة الحسابات
  path('signup/', SignUpView.as_view(), name='signup'),
  path('profile/', ProfileUpdateView.as_view(), name='profile'),
  path('password-change/', PasswordChangeRTLView.as_view(), name='password_change'),

  # وثائق الشركات
  path('documents/add/', CompanyDocumentCreateView.as_view(), name='add_document'),
  path('documents/<int:pk>', views.CompanyDocumentDetailView.as_view(), name='document_detail'),

  # إدارة اللغة والاتجاه
  path('set-language/', set_language, name='set_language'),
  path('toggle-rtl/', views.toggle_rtl, name='toggle_rtl'),

  # مسارات خاصة بأنواع المستخدمين
  path('owner/dashboard/', views.BuildingOwnerDashboard.as_view(), name='owner_dashboard'),
  path('investor/dashboard/', views.InvestorDashboard.as_view(), name='investor_dashboard'),
  path('company/dashboard/', views.RentalCompanyDashboard.as_view(), name='company_dashboard'),

  # API Endopints
  path('api/user-type/', views.UserTypeAPIView.as_view(), name='user_type_api'),
]

# اسماء المترجمة
app_name = 'accounts'