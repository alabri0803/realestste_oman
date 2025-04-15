from django.urls import path
from django.views.i18n import set_language

from . import views
from .views import (
    CompanyDocumentCreateView,
    CompanyDocumentListView,
    CompanyDocumentDetailView,
    CustomLoginView,
    CustomLogoutView,
    PasswordChangeRTLView,
    ProfileUpdateView,
    SignUpView,
    BuildingOwnerDashboard,
    InvestorDashboard,
    RentalCompanyDashboard,
    UserTypeAPIView,
)

urlpatterns = [
    # مصادقة المستخدمين
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # إدارة الحسابات
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('password-change/', PasswordChangeRTLView.as_view(), name='password_change'),

    # وثائق الشركات
    path('documents/', CompanyDocumentListView.as_view(), name='document_list'),
    path('documents/add/', CompanyDocumentCreateView.as_view(), name='add_document'),
    path('documents/<int:pk>/', CompanyDocumentDetailView.as_view(), name='document_detail'),

    # إدارة اللغة والاتجاه
    path('set-language/', set_language, name='set_language'),
    path('toggle-rtl/', views.toggle_rtl, name='toggle_rtl'),

    # مسارات خاصة بأنواع المستخدمين
    path('owner/dashboard/', BuildingOwnerDashboard.as_view(), name='owner_dashboard'),
    path('investor/dashboard/', InvestorDashboard.as_view(), name='investor_dashboard'),
    path('company/dashboard/', RentalCompanyDashboard.as_view(), name='company_dashboard'),

    # API Endpoints
    path('api/user-type/', UserTypeAPIView.as_view(), name='user_type_api'),
]

# اسم التطبيق
app_name = 'accounts'