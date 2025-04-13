from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
  model = UserProfile
  can_delete = False
  verbose_name_plural = 'الملف الشخصي'

class CustomUserAdmin(UserAdmin):
  inlines = (UserProfileInline,)
  list_display = ('username', 'email', 'get_role', 'is_staff')

  def get_role(self, obj):
    return obj.userprofile.role if hasattr(obj, 'userprofile') else 'غير محدد'
  get_role.short_description = 'الدور'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)