from django.shortcuts import render

from .models import Unit


def home(request):
  return render(request, 'rentals/home.html')

def units_list(request):
  units = Unit.objects.all()
  return render(request, 'rentals/units_list.html', {'units': units})

def new_page(request):
  return render(request, 'rentals/new_page.html')