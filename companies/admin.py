from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
  list_display = ('name', 'commercial_registration', 'contact_person', 'phone')
  search_fields = ('name', 'commercial_registration')
  readonly_fields = ('logo_preview',)

  def logo_preview(self, obj):
    if obj.logo:
      return f'<img src="{obj.logo.url}" width="100" />'
    return 'لا يوجد شعار'
  logo_preview.allow_tags = True
  logo_preview.short_description = 'معاينة الشعار'