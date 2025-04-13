from django.db import models

from companies.models import Company


class Building(models.Model):
  name = models.CharField(max_length=100, verbose_name='اسم المبنى')
  address = models.TextField(verbose_name='العنوان')
  total_floors = models.IntegerField(verbose_name='عدد الطوابق')
  description = models.TextField(blank=True, verbose_name='وصف المبنى')

  class Meta:
    verbose_name = 'مبنى'
    verbose_name_plural = 'المباني'

  def __str__(self):
    return self.name
  
class Unit(models.Model):
  UNIT_TYPES = [
    ('shop', 'محل تجاري'),
    ('office', 'مكتب'),
    ('apartment', 'شقة'),
    ('storage', 'مخزن'),
    ('parking', 'موقف سيارات')
  ]
  building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name='المبنى')
  unit_type = models.CharField(max_length=20, choices=UNIT_TYPES, verbose_name='نوع الوحدة')
  unit_number = models.CharField(max_length=20, verbose_name='رقم الوحدة')
  area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المساحة')
  monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='الإيجار الشهري (ريال عماني)')
  is_occupied = models.BooleanField(default=False, verbose_name='مؤجرة؟')

  class Meta:
    verbose_name = 'وحدة'
    verbose_name_plural = 'الوحدات'

  def __str__(self):
    return f"{self.unit_number} - {self.get_unit_type_display()}"

class LeaseContract(models.Model):
  company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='الشركة')
  unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name='الوحدة')
  start_date = models.DateField(verbose_name='تاريخ البدء')
  end_date = models.DateField(verbose_name='تاريخ الانتهاء')
  monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='الإيجار الشهري (ريال عماني)')
  deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قيمة الضمان (ريال عماني)')
  contract_file = models.FileField(upload_to='contracts/', verbose_name='ملف العقد')

  class Meta:
    verbose_name = 'عقد إيجار'
    verbose_name_plural = 'عقود الإيجار'

  def __str__(self):
    return f"عقد {self.company.name} - {self.unit.unit_number}"