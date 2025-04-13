from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
  ROLES = (
    ('admin', 'مدير النظام'),
    ('accountant', 'محاسب'),
    ('viewer', 'مشاهد')
  )
  user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='المستخدم')
  phone = models.CharField(max_length=20, verbose_name='رقم الهاتف')
  role = models.CharField(max_length=50, choices=ROLES, verbose_name='الدور')

  def __str__(self):
    return f"{self.user.username} - {self.get_role_display()}"
