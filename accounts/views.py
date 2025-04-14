from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, TemplateView, CreateView, UpdateView, DetailView, ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile, CompanyDocument
from .forms import CustomUserCreationForm, UserProfileForm, CompanyDocumentForm, LoginForm
from django.contrib.auth.views import PasswordChangeView

class BaseRTLView:
  """
  كلاس أساسي لإعدادات والترجمة
  """
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['rtl'] = True
    context['lang'] = 'ar'
    context['dir'] = 'rtl'
    context['page_title'] = getattr(self, 'page_title', _('نظام الإيجارات'))
    return context

# مصادقة المستخدمين
class CustomLoginView(BaseRTLView, View):
  """
  واجهة تسجيل الدخول مع دعم الترجمة
  """
  template_name = 'accounts/login.html'
  page_title = _('تسجيل الدخول')

  def get(self, request):
    form = LoginForm()
    return render(request, self.template_name, {
      'form': form,
      **self.get_context_data()
    })

  def post(self, request):
    form = LoginForm(request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect(self.get_redirect_url(user))
    return render(request, self.template_name, {
      'form': form,
      **self.get_context_data()
    })

  def get_redirect_url(self, user):
    if user.user_type == 'owner':
      return reverse_lazy('owner_dashboard')
    elif user.user_type == 'investor':
      return reverse_lazy('investor_dashboard')
    return reverse_lazy('company_dashboard')

class CustomLogoutView(View):
  """
  واجهة تسجيل الخروج
  """
  def get(self, request):
    logout(request)
    return redirect('login')

# إدارة الحسابات
class SignUpView(BaseRTLView, CreateView):
  """
  واجهة تسجيل مستخدم جديد مع تحديد نوع الحساب
  """
  model = CustomUser
  form_class = CustomUserCreationForm
  template_name = 'accounts/signup.html'
  success_url = reverse_lazy('login')
  page_title = _('تسجيل حساب جديد')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['user_types'] = [
      (_('owner'), _('مالك المبني')),
      (_('investor'), _('مستثمر المبني')),
      (_('company'), _('شركة مستأجرة')),
    ]
    return context

class ProfileUpdateView(LoginRequiredMixin, BaseRTLView, UpdateView):
  """
  واجهة تحديث الملف الشخصي مع دعم ثنائي اللغة
  """
  model = CustomUser
  form_class = UserProfileForm
  template_name = 'accounts/profile.html'
  success_url = reverse_lazy('profile')
  page_title = _('الملف الشخصي')

  def get_object(self):
    return self.request.user

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['instance'] = self.request.user.profile
    return kwargs

# لوحة التحكم
class BuildingOwnerDashboard(LoginRequiredMixin, UserPassesTestMixin, BaseRTLView, TemplateView):
  """
  لوحة التحكم مالك المبني
  """
  template_name = 'accounts/dashboards/owner.html'
  page_title = _('لوحة التحكم - مالك المبني')

  def test_func(self):
    return self.request.user.user_type == 'owner'

class InvestorDashboard(LoginRequiredMixin, UserPassesTestMixin, BaseRTLView, TemplateView):
  """
  لوحة التحكم المستثمر
  """
  template_name = 'accounts/dashboards/investor.html'
  page_title = _('لوحة التحكم - المستثمر')

  def test_func(self):
    return self.request.user.user_type == 'investor'

class RentalCompanyDashboard(LoginRequiredMixin, UserPassesTestMixin, BaseRTLView, TemplateView):
  """
  لوحة التحكم شركة المستأجرة
  """
  template_name = 'accounts/dashboards/company.html'
  page_title = _('لوحة التحكم - شركة المستأجرة')

  def test_func(self):
    return self.request.user.user_type == 'company'

# إدارة الوثائق
class CompanyDocumentCreateView(LoginRequiredMixin, BaseRTLView, CreateView):
  """
  واجهة رفع وثائق الشركة
  """
  model = CompanyDocument
  form_class = CompanyDocumentForm
  template_name = 'accounts/documents/add.html'
  success_url = reverse_lazy('profile')
  page_title = _('إضافة وثيقة')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['user_type'] = self.request.user.user_type
    return kwargs

class CompanyDocumentListView(LoginRequiredMixin, BaseRTLView, ListView):
  """
  قائمة وثائق الشركة
  """
  model = CompanyDocument
  template_name = 'accounts/documents/list.html'
  context_object_name = 'documents'
  page_title = _('وثائق الشركة')

  def get_queryset(self):
    return CompanyDocument.objects.filter(user=self.request.user)

# خدمات المساعدة
class PasswordChangeRTLView(BaseRTLView, PasswordChangeView, LoginRequiredMixin):
  """
  واجهة تغيير كلمة المرور مع دعم الترجمة
  """
  template_name = 'accounts/password_change.html'
  success_url = reverse_lazy('profile')
  page_title = _('تغيير كلمة المرور')

class LanguageToggleView(View):
  """
  واجهة تبديل اللغة
  """
  def post(self, request):
    lang = 'ar' if request.LANGUAGE_CODE == 'en' else 'en'
    request.session['django_language'] = lang
    return redirect(request.META.get('HTTP_REFERER', '/'))