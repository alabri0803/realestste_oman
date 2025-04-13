from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .forms import CompanyForm
from .models import Company


class CompanyListView(ListView):
  model = Company
  template_name = 'companies/company_list.html'
  paginate_by = 15

def company_detail(request, pk):
  company = get_object_or_404(Company, pk=pk)
  contracts = company.leasecontract_set.all()
  return render(request, 'companies/company_detail.html', {'company': company, 'contracts': contracts})

def company_create(request):
  if request.method == 'POST':
    form = CompanyForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('company_list')
  else:
    form = CompanyForm()
  return render(request, 'companies/company_form.html', {'form': form})

def company_update(request, pk):
  company = get_object_or_404(Company, pk=pk)
  if request.method == 'POST':
    form = CompanyForm(request.POST, request.FILES, instance=company)
    if form.is_valid():
      form.save()
      return redirect('company_detail', pk=company.pk)
  else:
    form = CompanyForm(instance=company)
  return render(request, 'companies/company_form.html', {'form': form})

def company_delete(request, pk):
  company = get_object_or_404(Company, pk=pk)
  if request.method == 'POST':
    company.delete()
    return redirect('company_list')