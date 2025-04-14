from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import Http404, request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, TemplateView, View, UpdateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import (
  CompanyDocumentForm,
  CustomUserChangeForm,
  CustomUserCreationForm,
  LoginForm,
  UserProfileForm,
)
from .models import CompanyDocument, CustomUser


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

def toggle_rtl(request):
  """
  دالة لتبديل وضع RTL/LTR وحفظه في الجلسة
  """
  if 'rtl_mode' not in request.session:
      request.session['rtl_mode'] = True if get_language() == 'ar' else False

  request.session['rtl_mode'] = not request.session['rtl_mode']
  referer = request.META.get('HTTP_REFERER', '/')
  return redirect(referer)
  
# مصادقة المستخدمين
class CustomLoginView(BaseRTLView, View):
  """
  واجهة تسجيل الدخول مع دعم الترجمة
  """
  template_name = 'accounts/login.html'
  page_title = _('تسجيل الدخول')

  def get_context_data(self, **kwargs):
    return {'page_title': self.page_title,}

  def get(self, request):
    form = LoginForm()
    return render(request, self.template_name, {
      'form': form,
      **self.get_context_data()
    })

  def post(self, request):
    form = AuthenticationForm(request, data=request.POST)
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
      return reverse_lazy('accounts:owner_dashboard')
    elif user.user_type == 'accounts:investor':
      return reverse_lazy('investor_dashboard')
    return reverse_lazy('accounts:company_dashboard')

class CustomLogoutView(View):
  """
  واجهة تسجيل الخروج
  """
  def get(self, request):
    logout(request)
    return redirect('accounts:login')

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
  success_url = reverse_lazy('accounts:profile')
  page_title = _('الملف الشخصي')

  def get(self, request, *args, **kwargs):
    user_form = CustomUserChangeForm(instance=self.request.user)
    profile_form = UserProfileForm(instance=self.request.user.profile)
    return render(request, self.template_name, self.get_context_data(
      user_form=user_form,
      profile_form=profile_form
    ))

  def post(self, request, *args, **kwargs):
    user_form = CustomUserChangeForm(request.POST, instance=self.request.user)
    profile_form = UserProfileForm(request.POST, request.FILES, instance=self.request.user.profile)
    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      return redirect('accounts:profile')
    return render(request, self.template_name, self.get_context_data(
      user_form=user_form,
      profile_form=profile_form
    ))

  def get_context_data(self, **kwargs):
    context = kwargs
    context['documents'] = CompanyDocument.objects.filter(user=self.request.user)[:3]
    return context

# لوحة التحكم
class BuildingOwnerDashboard(LoginRequiredMixin, UserPassesTestMixin, BaseRTLView, TemplateView):
  """
  لوحة التحكم مالك المبني
  """
  template_name = 'accounts/dashboards/owner_dashboard.html'
  page_title = _('لوحة التحكم - مالك المبني')

  def test_func(self):
    return self.request.user.user_type == 'owner'

class InvestorDashboard(LoginRequiredMixin, UserPassesTestMixin, BaseRTLView, TemplateView):
  """
  لوحة التحكم المستثمر
  """
  template_name = 'accounts/dashboards/investor_dashboard.html'
  page_title = _('لوحة التحكم - المستثمر')

  def test_func(self):
    return self.request.user.user_type == 'investor'

class RentalCompanyDashboard(LoginRequiredMixin, UserPassesTestMixin, BaseRTLView, TemplateView):
  """
  لوحة التحكم شركة المستأجرة
  """
  template_name = 'accounts/dashboards/company_dashboard.html'
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
  success_url = reverse_lazy('accounts:profile')
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

class CompanyDocumentDetailView(LoginRequiredMixin, UserPassesTestMixin, BaseRTLView, DetailView):
  """
  واجهة عرض تفاصيل وثيقة الشركة مع تحقق من صلاحيات المستخدم ويدعم الترجمة
  """
  model = CompanyDocument
  template_name = 'accounts/documents/detail.html'
  context_object_name = 'document'
  page_title = _('تفاصيل الوثيقة')

  def test_func(self):
    """
    تحقق من أن المستخدم عرض الوثيقة
    """
    document = self.get_object()
    user = self.request.user

    # المالك يمكنه رؤية جميع الوثائق المبني
    if user.user_type == 'owner':
      return True
    # المستثمر يمكنه رؤية جميع الوثائق المبني
    elif user.user_type == 'investor':
      return document.building.owner == user
    # الشركة يمكنها رؤية وثائقها فقط
    elif user.user_type == 'company':
      return document.company == user
    return False

  def get_object(self):
    """
    استرجاع الوثيقة مع التحقق من وجودها
    """
    try:
      doc = super().get_object(request)
      # تحقق إضافي من أن الوثيقة تابعة للمستخدم الحالي
      if doc.user != self.request.user:
        raise Http404(_('لا تملك صلاحية عرض هذه الوثيقة.'))
      return doc
    except CompanyDocument.DoesNotExist:
      raise Http404(_('الوثيقة غير موجودة.'))

  def get_context_data(self, **kwargs):
    """
    إضافة بيانات إضافية للقالب
    """
    context = super().get_context_data(**kwargs)
    document = self.get_object()

    # بيانات إضافية حسب نوع المستخدم
    if self.request.user.user_type == 'owner':
      context['can_edit'] = True
      context['can_delete'] = True
    else:
      context['can_edit'] = document.user == self.request.user
      context['can_delete'] = document.user == self.request.user

    # معلومات ملف المرفق
    context['file_url'] = {
      'name': document.file.name.split('/')[-1],
      'size': f"{document.file.size / 1024:.1f} KB",
      'type': document.get_document_type_display()
    }

    # إضافة زر العودة المناسب
    if self.request.user.user_type == 'owner':
      context['back_url'] = reverse_lazy('accounts:owner_dashboard')
    else:
      context['back_url'] = reverse_lazy('accounts:document_list')
    return context

  def handle_no_permission(self):
    """
    معالجة حالة عدم وجود صلاحيات
    """
    if self.request.user.is_authenticated:
      messages.error(self.request, _('لا تملك صلاحية عرض هذه الوثيقة.'))
      return redirect('accounts:profile')
    return super().handle_no_permission()

# خدمات المساعدة
class PasswordChangeRTLView(BaseRTLView, PasswordChangeView, LoginRequiredMixin):
  """
  واجهة تغيير كلمة المرور مع دعم الترجمة
  """
  template_name = 'accounts/password_change.html'
  success_url = reverse_lazy('accounts:profile')
  page_title = _('تغيير كلمة المرور')

class LanguageToggleView(View):
  """
  واجهة تبديل اللغة
  """
  def post(self, request):
    lang = 'ar' if request.LANGUAGE_CODE == 'en' else 'en'
    request.session['django_language'] = lang
    return redirect(request.META.get('HTTP_REFERER', '/'))

# API
class UserTypeAPIView(APIView):
  """
  واجهة API لاسترجاع نوع المستخدم
  """
  def get(self, request):
    user_types = [
      {
        'value': 'owner',
        'label': _('مالك المبني'),
        'description': _('المالك القانوني للمبني للتجاري')
      },
      {
        'value': 'investor',
        'label': _('مستثمر المبني'),
        'description': _('طرف مستثمر في المبني له حقوق استثمارية')
      },
      {
        'value': 'company',
        'label': _('شركة مستأجرة'),
        'description': _('شركة لديها عقد إيجار لوحدات في المبني')
      }
    ]
    return Response({
      'success': True,
      'data': user_types,
      'message': _('تم جلب أنواع المستخدمين بنجاح.')
    }, status=status.HTTP_200_OK)
    
  def post(self, request):
    user_type = request.data.get('user_type')
    if user_type not in ['owner', 'investor', 'company']:
      return Response({
        'success': False,
        'message': _('نوع المستخدم غير صالح.')
      }, status=status.HTTP_400_BAD_REQUEST)
    request.session['user_type'] = user_type