from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from modeltranslation.fields import TranslationField

class Building(models.Model):
  """
  نموذج يمثل المباني التجارية
  """
  name = models.CharField(
    max_length=100, 
    verbose_name=_('اسم المبنى')
  )
  address = models.TextField(
    verbose_name=_('العنوان التفصيلي')
  )
  total_floors = models.PositiveIntegerField(
    verbose_name=_('عدد الطوابق')
  )
  description = models.TextField(
    blank=True, 
    verbose_name=_('وصف المبنى')
  )

  # حقول التتبع
  created_at = models.DateTimeField(
    auto_now_add=True, 
    verbose_name=_('تاريخ الإنشاء')
  )
  updated_at = models.DateTimeField(
    auto_now=True, 
    verbose_name=_('تاريخ التحديث')
  )

  # الترجمة
  #translations = TranslationField(fields=('name''description'))

  class Meta:
    verbose_name = _('المبني')
    verbose_name_plural = _('المباني')
    ordering = ['name']

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('building_detail', kwargs={'pk': self.pk})
  
class Unit(models.Model):
  """
  نموذج يمثل الوحدات داخل المبني (محلات، مكاتب، إلخ)
  """
  UNIT_TYPES = [
    ('shop', _('محل تجاري')),
    ('office', _('مكتب')),
    ('apartment', _('شقة')),
    ('storage', _('مخزن')),
    ('parking', _('موقف سيارات'))
  ]
  building = models.ForeignKey(
    Building, 
    on_delete=models.CASCADE, 
    verbose_name=_('المبنى'),
    related_name='units'
  )
  unit_type = models.CharField(
    max_length=20, 
    choices=UNIT_TYPES, 
    verbose_name=_('نوع الوحدة')
  )
  unit_number = models.CharField(
    max_length=20, 
    verbose_name=_('رقم الوحدة'))
  area = models.DecimalField(
    max_digits=10, 
    decimal_places=2, 
    verbose_name=_('المساحة')
  )
  monthly_rent = models.DecimalField(
    max_digits=10, 
    decimal_places=2, 
    verbose_name=_('الإيجار الشهري (ريال عماني)')
  )
  is_occupied = models.BooleanField(
    default=False, 
    verbose_name=_('مؤجرة؟')
  )

  # حقول التتبع
  created_at = models.DateTimeField(
    auto_now_add=True, 
    verbose_name=_('تاريخ الإنشاء')
  )
  updated_at = models.DateTimeField(
    auto_now=True, 
    verbose_name=_('تاريخ التحديث')
  )

  class Meta:
    verbose_name = _('الوحدة')
    verbose_name_plural = _('الوحدات')
    ordering = ['building', 'unit_number']
    unique_together = ('building', 'unit_number')
    
  def __str__(self):
    return f"{self.unit_number} - {self.get_unit_type_display()}"

  def get_absolute_url(self):
    return reverse('unit_detail', kwargs={'pk': self.pk})
    
class LeaseContract(models.Model):
  company = models.ForeignKey(
    'companies.Company', 
    on_delete=models.PROTECT, 
    verbose_name=_('الشركة المستأجرة')
  )
  unit = models.ForeignKey(
    Unit, 
    on_delete=models.PROTECT, 
    verbose_name=_('الوحدة')
  )
  start_date = models.DateField(
    verbose_name=_('تاريخ البدء')
  )
  end_date = models.DateField(
    verbose_name=_('تاريخ الانتهاء')
  )
  monthly_rent = models.DecimalField(
    max_digits=10, 
    decimal_places=2, 
    verbose_name=_('الإيجار الشهري (ريال عماني)')
  )
  deposit_amount = models.DecimalField(
    max_digits=10, 
    decimal_places=2, 
    verbose_name=_('قيمة الضمان (ريال عماني)')
  )
  contract_file = models.FileField(
    upload_to='contracts/%Y/%m/', 
    verbose_name=_('ملف العقد')
  )
  notes = models.TextField(
    blank=True, 
    verbose_name=_('ملاحظات')
  )

  # حقول التتبع
  created_at = models.DateTimeField(
    auto_now_add=True, 
    verbose_name=_('تاريخ الإنشاء')
  )
  updated_at = models.DateTimeField(
    auto_now=True, 
    verbose_name=_('تاريخ التحديث')
  )

  # الترجمة
  #translations = TranslationField(fields=('notes',))

  class Meta:
    verbose_name = _('عقد إيجار')
    verbose_name_plural = _('عقود الإيجار')
    ordering = ['-start_date']

  def __str__(self):
    return f"عقد {self.company.name} - {self.unit.unit_number}"

  def get_absolute_url(self):
    return reverse('contract_detail', kwargs={'pk': self.pk})

  def clean(self):
    from django.core.exceptions import ValidationError
    if self.end_date <= self.start_date:
      raise ValidationError(_('تاريخ الانتهاء يجب أن يكون بعد تاريخ البدء.'))
    if self.unit.is_occupied:
      raise ValidationError(_('الوحدة مؤجرة بالفعل.'))

  def save(self, *args, **kwargs):
    self.full_clean()
    super().save(*args, **kwargs)
    self.unit.is_occupied = True
    self.unit.save()