from django.shortcuts import render
from django.utils import timezone

from rentals.models import LeaseContract


def financial_report(request):
  year = request.GET.get('year', timezone.now().year)
  contracts = LeaseContract.objects.filter(start_date__year=year)
  return render(request, 'reports/financial_report.html', {'date': date})

def occupancy_report(request):
  year = request.GET.get('year', timezone.now().year)
  contracts = LeaseContract.objects.filter(start_date__year=year)
  return render(request, 'reports/occupancy_report.html', {'date': date})

def export_data(request):
  return render(request, 'reports/export_data.html')