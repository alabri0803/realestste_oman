from django import forms

from .models import Invoice, Payment


class PaymentForm(forms.ModelForm):
  class Meta:
    model = Payment
    fields = ['contract', 'amount', 'payment_date', 'payment_method', 'receipt_number']
    widgets = {
      'payment_date': forms.DateInput(attrs={'type': 'date'}),
      'payment_method': forms.Select(choices=Payment.PAYMENTS_METHODS),
    }

class InvoiceForm(forms.ModelForm):
  class Meta:
    model = Invoice
    fields = ['payment', 'due_date', 'status']
    widgets = {
      'due_date': forms.DateInput(attrs={'type': 'date'}),
    }