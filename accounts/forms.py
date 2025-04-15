from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

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
            'email',
            'user_type',
            'phone',
            'arabic_name',
            'english_name',
        )
        labels = {
            'email': _('البريد الإلكتروني'),
            'user_type': _('نوع الحساب'),
            'phone': _('الهاتف'),
            'arabic_name': _('الاسم بالعربية'),
            'english_name': _('الاسم بالإنجليزية'),
        }
        widgets = {
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('+968XXXXXXXX')
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('البريد الإلكتروني')
                }
            ),
            'user_type': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'arabic_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('الاسم بالعربية'),
                    'dir': 'rtl'
                }
            ),
            'english_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('الاسم بالإنجليزية'),
                    'dir': 'ltr'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # إزالة حقل username من النموذج
        if 'username' in self.fields:
            del self.fields['username']


class CustomUserChangeForm(UserChangeForm):
    """
    نموذج تعديل بيانات المستخدم
    """
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'phone',
            'arabic_name',
            'english_name',
        )
        labels = {
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
                    'dir': 'rtl'
                }
            ),
            'address_english': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'dir': 'ltr'
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

    def clean(self):
        cleaned_data = super().clean()
        issue_date = cleaned_data.get('issue_date')
        expiry_date = cleaned_data.get('expiry_date')

        if issue_date and expiry_date and expiry_date < issue_date:
            raise ValidationError(_('تاريخ الانتهاء يجب أن يكون بعد تاريخ الإصدار'))


class LoginForm(forms.Form):
    """
    نموذج تسجيل الدخول المخصص
    """
    username = forms.CharField(
        label=_('البريد الإلكتروني أو رقم الهاتف'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('البريد الإلكتروني أو رقم الهاتف'),
                'autofocus': True  # تصحيح الخطأ الإملائي هنا
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