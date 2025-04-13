from django import forms

from .models import Building, LeaseContract, Unit


class BuildingForm(forms.ModelForm):
  class Meta:
    model = Building
    fields = ['name', 'address', 'total_floors', 'description']
    widgets = {
      'description': forms.Textarea(attrs={'rows': 3}),
    }

class UnitForm(forms.ModelForm):
  class Meta:
    model = Unit
    fields = ['building', 'unit_type', 'unit_number', 'area', 'monthly_rent']
    widgets = {
      'unit_type': forms.Select(attrs={'class': 'form-control'}),
    }

class LeaseContractForm(forms.ModelForm):
  class Meta:
    model = LeaseContract
    fields = ['company', 'unit', 'start_date', 'end_date', 'monthly_rent', 'deposit_amount', 'contract_file']
    widgets = {
      'start_date': forms.DateInput(attrs={'type': 'date'}),
      'end_date': forms.DateInput(attrs={'type': 'date'}),
    }

    def clean(self):
      cleaned_data = super().clean()
      start_date = cleaned_data.get('start_date')
      end_date = cleaned_data.get('end_date')
      if end_date <= start_date:
        raise forms.ValidationError('تاريخ الانتهاء يجب أن يكون بعد تاريخ البدء')