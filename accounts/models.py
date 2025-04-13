from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
  """
  نموذج المستخدم المخصص الذي يرث من AbstractUser
  يدعم أنواع المستخدمين المختلفة مثل (مالك العقار، شركة، موظف)
  """
  # أنواع المستخدمين (يدعم الترجمة)
  class UserTypes(models.TextChoices):
    BUILDING_OWNER = 'owner', _('مالك المبني')
    INVESTOR = 'investor', _('مستثمر')
    RENTAL_COMPANY = 'company', _('شركة مستأجرة')

  # حقول إضافية
  user_type = models.CharField(
    max_length=10,
    choices=UserTypes.choices,
    verbose_name=_('نوع المستخدم'),
    default=UserTypes.RENTAL_COMPANY
  )

  phone_regex = RegexValidator(
    regex=r'^\+968\d{8}$',
    message=_("رقم الهاتف يجب أن يكون بتنسيق: +968XXXXXXXX.")
  )
  phone = models.CharField(
    validators=[phone_regex],
    max_length=12,
    verbose_name=_('هاتف عماني'),
    blank=True,
    null=True
  )

  arabic_name = models.CharField(
    max_length=100,
    verbose_name=_('الاسم بالعربية'),
    blank=True
  )

  english_name = models.CharField(
    max_length=100,
    verbose_name=_('الاسم بالإنجليزية'),
    blank=True
  )

  commercial_registration = models.CharField(
    max_length=50,
    verbose_name=_('السجل التجاري'),
    blank=True,
    null=True,
    unique=True
  )

  is_verified = models.BooleanField(
    default=False,
    verbose_name=_('حساب موثوق')
  )

  class Meta:
    verbose_name = _('مستخدم')
    verbose_name_plural = _('المستخدمون')
    ordering = ['-date_joined']

  def __str__(self):
    return self.arabic_name or self.username

class UserProfile(models.Model):
  """
  نموذج الملف الشخصي الموسع للمستخدمين
  """
  user = models.OneToOneField(
    CustomUser,
    on_delete=models.CASCADE,
    related_name='profile',
    verbose_name=_('المستخدم')
  )

  address_arabic = models.TextField(
    verbose_name=_('العنوان بالعربية'),
    blank=True
  )

  address_english = models.TextField(
    verbose_name=_('العنوان بالإنجليزية'),
    blank=True
  )

  logo = models.ImageField(
    upload_to='users/logos/',
    verbose_name=_('الشعار'),
    blank=True,
    null=True
  )

  class Meta:
    verbose_name = _('ملف شخصي')
    verbose_name_plural = _('الملفات الشخصية')

  def __str__(self):
    return f"{self.user.arabic_name} - {self.user.get_user_type_display()}"

class CompanyDocument(models.Model):
  """
  نموذج لحفظ وثائق الشركات (للمستأجرين والمستثمرين)
  """
  user = models.ForeignKey(
    CustomUser,
    on_delete=models.CASCADE,
    related_name='documents',
    verbose_name=_('المستخدم')
  )

  DOCUMENT_TYPES = (
    ('commercial_license', _('رخصة تجارية')),
    ('id_copy', _('نسخة بطاقة')),
    ('contract', _('عقد التأسيس')),
  )

  document_type = models.CharField(
    max_length=50,
    choices=DOCUMENT_TYPES,
    verbose_name=_('نوع المستند')
  )

  file = models.FileField(
    upload_to='company_documents/',
    verbose_name=_('الملف')
  )

  issue_date = models.DateField(
    verbose_name=_('تاريخ الإصدار'),
    blank=True,
    null=True
  )

  expiry_date = models.DateField(
    verbose_name=_('تاريخ الانتهاء'),
    blank=True,
    null=True
  )

  class Meta:
    verbose_name = _('وثيقة شركة')
    verbose_name_plural = _('وثائق الشركات')
    ordering = ['-issue_date']

  def __str__(self):
    return f"{self.get_document_type_display()} - {self.user.arabic_name}"