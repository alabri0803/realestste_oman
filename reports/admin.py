from django.contrib import admin

from .models import FinancialReport


@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
  list_display = ('title', 'period', 'generated_by', 'created_at')
  list_filter = ('period', 'generated_by')
  readonly_fields = ('created_at',)