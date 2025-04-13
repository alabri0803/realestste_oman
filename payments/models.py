from django.db import models


class Payment(models.Model):
  PAYMENTS_METHODS = (
    ('bank', 'تحويل بنكي'),
    ('cash', 'نقدي'),
    ('check', 'شيك')
  )
  contract = models.ForeignKey('rentals.LeaseContract', on_delete=models.CASCADE, verbose_name='العقد')
  amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المبلغ (ريال عماني)')
  payment_date = models.DateField(verbose_name='تاريخ الدفع')
  payment_method = models.CharField(max_length=50, choices=PAYMENTS_METHODS, verbose_name='طريقة الدفع')
  receipt_number = models.CharField(max_length=50, unique=True, verbose_name='رقم الإيصال')

  class Meta:
    verbose_name = 'دفعة'
    verbose_name_plural = 'الدفعات'

  def __str__(self):
    return f"دفعة {self.amount} ريال - {self.contract}"

class Invoice(models.Model):
  payment = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name='الدفع')
  invoice_number = models.CharField(max_length=50, unique=True, verbose_name='رقم الفاتورة')
  issue_date = models.DateField(verbose_name='تاريخ الإصدار')
  due_date = models.DateField(verbose_name='تاريخ الاستحقاق')
  status = models.CharField(max_length=50, choices=(('paid', 'مسددة'), ('unpaid', 'غير مسددة')), verbose_name='الحالة')

  class Meta:
    verbose_name = 'فاتورة'
    verbose_name_plural = 'الفواتير'

  def __str__(self):
    return self.invoice_number