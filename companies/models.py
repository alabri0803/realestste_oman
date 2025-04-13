from django.db import models


class Company(models.Model):
  name = models.CharField(max_length=200, verbose_name='اسم الشركة')
  commercial_registration = models.CharField(max_length=50, unique=True, verbose_name='السجل التجاري')
  contact_person = models.CharField(max_length=100, verbose_name='الشخص المسؤول')
  phone = models.CharField(max_length=20, verbose_name='رقم الهاتف')
  email = models.EmailField(verbose_name='البريد الإلكتروني')
  logo = models.ImageField(upload_to='company_logos/', blank=True, verbose_name='شعار الشركة')

  def __str__(self):
    return self.name