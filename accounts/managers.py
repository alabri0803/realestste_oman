from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from .models import UserProfile  # تم نقل الاستيراد إلى هنا

class CustomUserManager(BaseUserManager):
    def _validate_required_fields(self, email, password, user_type, **extra_fields):
        if not email:
            raise ValueError(_('يجب تتقديم عنوان بريد إلكتروني صحيح'))
        if not password:
            raise ValueError(_('يجب إدخال كلمة مرور'))
        if user_type not in dict(self.model.UserTypes.choices).keys():  # تم إصلاح الشرط هنا
            raise ValueError(_('نوع المستخدم المحدد غير صحيح'))

    def create_user(self, email, password=None, user_type='tenant', **extra_fields):
        self._validate_required_fields(email, password, user_type, **extra_fields)
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        UserProfile.objects.create(user=user)  # تم إزالة الاستيراد من هنا
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('user_type', 'owner')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('المشرف يجب أن يكون is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('المشرف يجب أن يكون is_superuser=True.'))

        arabic_name = extra_fields.get('arabic_name', 'مدير النظام')
        if not arabic_name:
            raise ValueError(_('يجب إدخال الاسم بالعربية للمشرف.'))

        # التحقق من صحة user_type
        self._validate_required_fields(email, password, extra_fields['user_type'], **extra_fields)
        return self.create_user(email, password, **extra_fields)

    def get_owners(self):
        return self.filter(user_type='owner').select_related('profile')

    def get_investors(self):
        return self.filter(user_type='investor').select_related('profile')

    def get_tenant_companies(self):
        return self.filter(user_type='tenant').select_related('profile')

    def get_by_commercial_registration(self, register_number):
        return self.get(commercial_registration=register_number)

    def activate_user(self, user_id):
        try:
            user = self.get(id=user_id)
            user.is_active = True
            user.save(using=self._db)
            return user
        except self.model.DoesNotExist:
            raise ValueError(_('المستخدم غير موجود'))