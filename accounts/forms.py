
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import CompanyDocument, CustomUser, UserProfile


class CustomUserCreationForm(UserCreationForm):
  """
  نموذج إنشاء مستخدم مخصص مع حقول إضافة للأنواع المختلفة
  """
  password1 = forms.CharField(
    label=_('كلمة المرور'),
    widget=forms.PasswordInput(
      attrs={
        'class': 'form-control',
        'placeholder': _('كلمة المرور')
      }
    ),
    help_text=_('يجب أن تحتوي كلمة المرور على 8 أحرف على الأقل.')
  )
  password2 = forms.CharField(
    label=_('تأكيد كلمة المرور'),
    widget=forms.PasswordInput(
      attrs={
        'class': 'form-control',
        'placeholder': _('تأكيد كلمة المرور')
      }
    ),
  )
  class Meta:
    model = CustomUser
    fields = (
      'username', 
      'email', 
      'user_type', 
      'phone', 
      'arabic_name', 
      'english_name', 
    )
    labels = {
      'username': _('اسم المستخدم'),
      'email': _('البريد الإلكتروني'),
      'user_type': _('نوع الحساب'),
      'phone': _('الهاتف'),
      'arabic_name': _('الاسم بالعربية'),
      'english_name': _('الاسم بالإنجليزية'),
    }
    widgets = {
      'user_type': forms.Select(
        attrs={
          'class': 'form-select',
        }
      ),
      'phone': forms.TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': '+968XXXXXXXX'
        }
      ),
    }
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # تخصيص حقول حسب نوع المستخدم
    self.fields['user_type'].choices = [
      ('owner', _('مالك المبني')),
      ('investor', _('مستثمر المبني')),
      ('company', _('شركة مستأجرة')),
    ]

class CustomUserChangeForm(UserChangeForm):
  """
  نموذج تعديل بيانات المستخدم
  """
  class Meta:
    model = CustomUser
    fields = (
      'username', 
      'email',
      'phone',
      'arabic_name',
      'english_name',
    )
    labels = {
      'username': _('اسم المستخدم'),
      'email': _('البريد الإلكتروني'),
      'phone': _('الهاتف'),
      'arabic_name': _('الاسم بالعربية'),
      'english_name': _('الاسم بالإنجليزية'),
    }

class UserProfileForm(forms.ModelForm):
  """
  نموذج الملف الشخصي الموسع
  """
  class Meta:
    model = UserProfile
    fields = (
      'address_arabic',
      'address_english',
      'logo',
    )
    labels = {
      'address_arabic': _('العنوان بالعربية'),
      'address_english': _('العنوان بالإنجليزية'),
      'logo': _('الشعار الشركة'),
    }
    widgets = {
      'address_arabic': forms.Textarea(
        attrs={
          'class': 'form-control',
          'rows': 3,
          'dir':'rtl'
        }
      ),
      'address_english': forms.Textarea(
        attrs={
          'class': 'form-control',
          'rows': 3,
          'dir':'ltr'
        }
      ),
    }

class CompanyDocumentForm(forms.ModelForm):
  """
  نموذج رفع وثائق الشركة
  """
  class Meta:
    model = CompanyDocument
    fields = (
      'document_type',
      'file',
      'issue_date',
      'expiry_date',
    )
    labels = {
      'document_type': _('نوع المستند'),
      'file': _('رفع الملف'),
      'issue_date': _('تاريخ الإصدار'),
      'expiry_date': _('تاريخ الانتهاء'),
    }
    widgets = {
      'document_type': forms.Select(
        attrs={
          'class': 'form-select',
        }
      ),
      'issue_date': forms.DateInput(
        attrs={
          'class': 'form-control',
          'type': 'date'
        },
        format='%Y-%m-%d'
      ),
      'expiry_date': forms.DateInput(
        attrs={
          'class': 'form-control',
          'type': 'date'
        },
        format='%Y-%m-%d'
      ),
    }

class LoginForm(forms.Form):
  """
  نموذج تسجيل الدخول المخصص
  """
  username = forms.CharField(
    label=_('اسم المستخدم أو البريد الإلكتروني'),
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'placeholder': _('اسم المستخدم أو البريد الإلكتروني'),
        'autofocue': True
      }
    )
  )
  password = forms.CharField(
    label=_('كلمة المرور'),
    widget=forms.PasswordInput(
      attrs={
        'class': 'form-control',
        'placeholder': _('كلمة المرور')
      }
    )
  )
  remember_me = forms.BooleanField(
    label=_('تذكرني'),
    required=False,
    widget=forms.CheckboxInput(
      attrs={
        'class': 'form-check-input',
      }
    )
  )

class PasswordResetRequestForm(forms.Form):
  """
  نموذج طلب إعادة تعيين كلمة المرور
  """
  email = forms.EmailField(
    label=_('البريد الإلكتروني المسجل'),
    widget=forms.EmailInput(
      attrs={
        'class': 'form-control',
        'placeholder': _('أدخل بريدك الإلكتروني')
      }
    )
  )