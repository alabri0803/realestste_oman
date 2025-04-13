from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Company
from .forms import CompanyForm

class CompanyListView(ListView):
  model = Company
  template_name = 'companies/company_list.html'
  paginate_by = 15

def company_detail(request, pk):
  company = get_object_or_404(Company, pk=pk)
  contracts = company.leasecontract_set.all()
  return render(request, 'companies/company_detail.html', {'company': company, 'contracts': contracts})