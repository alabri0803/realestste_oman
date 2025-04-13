from django.db import models


class Building(models.Model):
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=200)
  total_floors = models.IntegerField()
  # ... معلومات أخرى عن المبنى

class Unit(models.Model):
  UNIT_TYPES = [
    ('shop', 'محل تجاري'),
    ('office', 'مكتب'),
    ('apartment', 'شقة'),
    ('storage', 'مخزن'),
    ('parking', 'موقف سيارات')
  ]
  building = models.ForeignKey(Building, on_delete=models.CASCADE)
  unit_type = models.CharField(max_length=20, choices=UNIT_TYPES)
  unit_number = models.CharField(max_length=20)
  area = models.DecimalField(max_digits=10, decimal_places=2)
  monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
  is_occupied = models.BooleanField(default=False)
  # ... معلومات أخرى عن الوحدة

class Company(models.Model):
  name = models.CharField(max_length=200)
  commercial_registration = models.CharField(max_length=50)
  contact_person = models.CharField(max_length=100)
  phone = models.CharField(max_length=20)
  email = models.EmailField()
  # ... معلومات أخرى عن الشركة

class LeaseContract(models.Model):
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
  start_date = models.DateField()
  end_date = models.DateField()
  monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
  deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
  contract_file = models.FileField(upload_to='contracts/')
  # ... شروط العقد الأخرى

class Payment(models.Model):
  contract = models.ForeignKey(LeaseContract, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  payment_date = models.DateField()
  payment_method = models.CharField(max_length=50)
  receipt_number = models.CharField(max_length=50)
  # ... معلومات الدفع الأخرى