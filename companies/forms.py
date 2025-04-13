from django import forms

from .models import Company


class CompanyForm(forms.ModelForm):
  commercial_registration = forms.CharField(
    label="السجل التجاري",
    help_text="يجب أن يكون رقم السجل فريداً",
  )

  class Meta:
    model = Company
    fields = ['name', 'commercial_registration', 'contact_person', 'phone', 'email', 'logo']