from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, FileExtensionValidator
from django.urls import reverse
from .managers import CustomUserManager

class CustomUser(AbstractUser):
  """
  نموذج المستخدم المخصص الذي يرث من AbstractUser
  يدعم أنواع المستخدمين المختلفة مثل (مالك العقار، شركة، موظف)
  """
  username = None
  first_name = None
  last_name = None
  # أنواع المستخدمين (يدعم الترجمة)
  class UserTypes(models.TextChoices):
    BUILDING_OWNER = 'owner', _('مالك المبني')
    INVESTOR = 'investor', _('مستثمر')
    TENANT_COMPANY = 'tenant', _('شركة المستأجر')

  class Meta:
    verbose_name = _('نوع المستخدم')
    verbose_name_plural = _('أنواع المستخدمين')

  email = models.EmailField(
    unique=True,
    help_text=_('يستخدم لتسجيل الدخول وإرسال الإشعارات')
  )

  # حقول إضافية
  user_type = models.CharField(
    _('نوع المستخدم'),
    max_length=10,
    choices=UserTypes.choices,
    default=UserTypes.TENANT_COMPANY,
    db_index=True
  )

  arabic_name = models.CharField(
    _('الاسم الكامل بالعربية'),
    max_length=150,
    help_text=_('الأسم كما يظهر في المستندات الرسمية')
  )

  english_name = models.CharField(
    _('الاسم الكامل بالإنجليزية'),
    max_length=150,
    help_text=_('مطلوب للشركات ذات التعاملات الدولية')
  )
  
  oman_phone_regex = RegexValidator(
    regex=r'^\+968\d{8}$',
    message=_("رقم الهاتف يجب أن يكون بتنسيق: +968XXXXXXXX.")
  )
  phone = models.CharField(
    _('هاتف عماني'),
    validators=[oman_phone_regex],
    max_length=12,
    unique=True,
  )

  commercial_register = models.CharField(
    _('السجل التجاري'),
    max_length=50,
    unique=True,
    blank=True,
    null=True,
    help_text=_('مطلوب للشركات و المستثمرين')
  )

  is_verified = models.BooleanField(
    _('حساب موثوق'),
    default=False,
    help_text=_('تم التحقق من المستندات الرسمية')
  )

  language = models.CharField(
    _('اللغة المفضلة'),
    max_length=2,
    choices=[('ar', _('العربية')), ('en', _('English'))],
    default='ar'
  )

  objects = CustomUserManager()

  groups = models.ManyToManyField(
    Group,
    verbose_name=_('المجموعات'),
    blank=True,
    related_name="custom_user_groups",
    help_text=_('تحديد صلاحيات المستخدم.'))

  user_permissions = models.ManyToManyField(
    Permission,
    verbose_name=_('الأذونات'),
    blank=True,
    related_name="custom_user_permissions",
    help_text=_('صلاحيات محددة لهذا المستخدم.')
  )

  class Meta:
    verbose_name = _('مستخدم')
    verbose_name_plural = _('المستخدمون')
    ordering = ['-date_joined']
    indexes = [
      models.Index(fields=['user_type']),
      models.Index(fields=['commercial_register']),
    ]

  def __str__(self):
    return f"{self.arabic_name} {self.get_user_type_display()}"

  def get_absolute_url(self):
    return reverse('accounts:profile', kwargs={'pk': self.pk})

  def clean(self):
    super().clean()
    if self.user_type in [self.UserTypes.INVESTOR, self.UserTypes.TENANT_COMPANY] and not self.commercial_register:
      raise ValidationError({
        'commercial_register': (_('مطلوب إدخال السجل التجاري لهذا النوع من الحسابات')})

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
    _('العنوان بالعربية'),
    max_length=500,
    help_text=_('الحي - الشارع - المدينة - الرمز البريد')
  )

  address_english = models.TextField(
    _('العنوان بالإنجليزية'),
    max_length=500,
    blank=True,
    help_text=_('مطلوب للشركات ذات العناوين الدولية')
  )

  twitter = models.URLField(
    _('حساب تويتر'),
    blank=True,
    null=True
  )

  linkedin = models.URLField(
    _('حساب لينكد إن'),
    blank=True,
    null=True
  )

  logo = models.ImageField(
    _('شعار الشركة/المؤسسة'),
    upload_to='users/logos/%Y/%m',
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
    blank=True,
    null=True
  )

  class Meta:
    verbose_name = _('ملف تعريفي')
    verbose_name_plural = _('الملفات التعريفية')

  def __str__(self):
    return _('ملف تعريفي') % self.user.arabic_name

class CompanyDocument(models.Model):
  """
  نموذج لحفظ وثائق الشركات (للمستأجرين والمستثمرين)
  """
  user = models.ForeignKey(
    CustomUser,
    on_delete=models.CASCADE,
    related_name='documents',
    verbose_name=_('المستخدم'),
    limit_choices_to={'user_type__in': ['investor', 'tenant']}
  )

  DOCUMENT_TYPES = (
    ('commercial_license', _('الرخصة التجارية')),
    ('article_of_association', _('عقد التأسيس')),
    ('owner_id', _('بطاقة هوية المالك')),
    ('lease_contract', _('عقد الإيجار')),
  )

  document_type = models.CharField(
    _('نوع المستند'),
    max_length=50,
    choices=DOCUMENT_TYPES,
  )

  file = models.FileField(
    _('رفع المستند'),
    upload_to='company_documents/%Y/%m',
    validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]
  )

  issue_date = models.DateField(
    _('تاريخ الإصدار'),
    blank=True,
    null=True
  )

  expiry_date = models.DateField(
    _('تاريخ الانتهاء'),
    blank=True,
    null=True
  )

  is_approved = models.BooleanField(
    _('موافق عليه'),
    default=False,
  )

  class Meta:
    verbose_name = _('وثيقة شركة')
    verbose_name_plural = _('وثائق الشركات')
    ordering = ['-issue_date']
    constraints = [
      models.UniqueConstraint(fields=['user', 'document_type'], name='unique_document_type_per_user')
    ]

  def __str__(self):
    return f"{self.get_document_type_display()} - {self.user.arabic_name}"

  def clean(self):
    if self.expiry_date and self.issue_date and self.expiry_date < self.issue_date:
      raise ValidationError(_('تاريخ الانتهاء يجب أن يكون بعد تاريخ الإصدار'))

class ActivityLog(models.Model):
  """
  نموذج لتسجيل نشاطات المستخدمين
  """
  user = models.ForeignKey(
    CustomUser,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    verbose_name=_('المستخدم')
  )

  action = models.CharField(
    _('الإجراء'),
    max_length=100
  )

  details = models.JSONField(
    _('التفاصيل'),
    default=dict,
  )

  ip_address = models.GenericIPAddressField(
    _('عنوان IP'),
    blank=True,
    null=True
  )

  created_at = models.DateTimeField(
    _('وقت الحدث'),
    auto_now_add=True
  )

  class Meta:
    verbose_name = _('سجل النشاط')
    verbose_name_plural = _('سجلات الانشطة')
    ordering = ['-created_at']

  def __str__(self):
    return f"{self.user} - {self.action}"