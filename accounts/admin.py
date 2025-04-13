from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CompanyDocument, CustomUser, UserProfile


class CustomUserAdmin(UserAdmin):
  """
  لوحة إدارة مخصصة لنموذج المستخدم مع دعم الترجمة
  """
  list_display = (
    'username',
    'arabic_name',
    'english_name',
    'user_type',
    'phone',
    'is_active'
  )
  list_filter = (
    'user_type',
    'is_active',
    'is_staff'
  )
  search_fields = (
    'username',
    'arabic_name',
    'english_name',
    'phone',
    'email'
  )
  ordering = ('-date_joined',)
  fieldsets = (
    (None, {'fields': ('username', 'password')}),
    (_('المعلومات الشخصية'), {'fields': (
      'arabic_name',
      'english_name',
      'email',
      'phone',
      'user_type'
    )}),
    (_('الصلاحيات'), {'fields': (
      'is_active',
      'is_staff',
      'is_superuser',
      'groups',
      'user_permissions'
    )}),
    (_('تواريخ مهمة'), {'fields': (
      'last_login',
      'date_joined'
    )}),
  )
  add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': (
          'username',
          'password1',
          'password2',
          'user_type'
        ),
    }),
  )
  def get_fieldsets(self, request, obj=None):
    fieldsets = super().get_fieldsets(request, obj)
    if not obj:
      fieldsets = self.add_fieldsets
    return fieldsets

  def get_list_display(self, request):
    if request.LANGUAGE_CODE == 'ar':
      return (
        'arabic_name',
        'user_type',
        'phone',
        'is_active'
      )
    return super().get_list_display(request)

class UserProfileAdmin(admin.ModelAdmin):
  """
  لوحة إدارة الملف الشخصي مع دعم الترجمة
  """
  list_display = (
    'user_arabic_name',
    'user_type',
    'short_address_ar',
    'short_address_en'
  )
  list_filter = (
    'user__user_type',
  )
  search_fields = (
    'user__arabic_name',
    'user__english_name',
    'address_arabic',
    'address_english'
  )
  raw_id_fields = ('user',)
  @admin.display(description=_('الاسم العربي'))
  def user_arabic_name(self, obj):
    return obj.user.arabic_name

  @admin.display(description=_('نوع المستخدم'))
  def user_type(self, obj):
    return obj.user.get_user_type_display()

  @admin.display(description=_('العنوان العربي'))
  def short_address_ar(self, obj):
    return obj.address_arabic[:30] + '...' if obj.address_arabic else ''

  @admin.display(description=_('العنوان الإنجليزي'))
  def short_address_en(self, obj):
    return obj.address_english[:30] + '...' if obj.address_english else ''

  class Media:
    css = {
      'all': ('css/admin-rtl.css',)
    }

class CompanyDocumentAdmin(admin.ModelAdmin):
  """
  لوحة إدارة وثائق الشركات مع تصفية حسب نوع المستخدم
  """
  list_display = (
    'document_type',
    'user_info',
    'issue_date',
    'expiry_date',
    'file_link'
  )
  readonly_fields = ('file_link',)
  
  @admin.display(description=_('معلومات المستخدم'))
  def user_info(self, obj):
    return f"{obj.user.arabic_name} ({obj.user.get_user_type_display()})"

  @admin.display(description=_('رابط الملف'))
  def file_link(self, obj):
    from django.utils.html import format_html
    if obj.file:
      return format_html('<a href="{}" target="_blank">{}</a>', obj.file.url, _('عرض الملف'))
    return _('لا يوجد ملف')
  fieldsets = (
    (None, {
        'fields': (
          'user', 
          'document_type'
        )
    }),
    (_('تفاصيل الملف'), {
        'fields': (
          'file',
          'file_link',
          'issue_date',
          'expiry_date'
        )
    }),
  )

  def get_queryset(self, request):
    qs = super().get_queryset(request)
    # تصفية حسب أنواع المستخدمين المطلوبة فقط
    return qs.filter(user__user_type__in=['owner', 'investor', 'company'])

# تسجيل النماذج
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CompanyDocument, CompanyDocumentAdmin)

# تعديل عناوين لوحة التحكم
admin.site.site_header = _('إدارة نظام الإيجارات - عمان')
admin.site.site_title = _('نظام إدارة العقارات')
admin.site.index_title = _('مرحبا بكم في لوحة التحكم')