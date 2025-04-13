from django.shortcuts import render
from django.utils import timezone

from rentals.models import LeaseContract


def financial_report(request):
  year = request.GET.get('year', timezone.now().year)
  contracts = LeaseContract.objects.filter(start_date__year=year)
  return render(request, 'reports/financial_report.html', {'date': date})