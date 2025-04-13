from django.contrib import admin

from .models import Invoice, Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
  list_display = ('contract', 'amount', 'payment_date', 'payment_method')
  list_filter = ('payment_date', 'payment_method')
  search_fields = ('contract__company__name', 'receipt_number')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
  list_display = ('invoice_number', 'payment', 'issue_date', 'due_date', 'status')
  list_filter = ('status', 'issue_date')
  search_fields = ('invoice_number',)