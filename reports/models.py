from django.db import models

from accounts.models import UserProfile


class FinancialReport(models.Model):
  title = models.CharField(max_length=200, verbose_name='عنوان التقرير')
  period = models.CharField(max_length=50, verbose_name='الفترة الزمنية')
  generated_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='منشأ بواسطة')
  report_file = models.FileField(upload_to='reports/', verbose_name='ملف التقرير')
  created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

  def __str__(self):
    return self.title