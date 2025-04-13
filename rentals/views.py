from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
  DetailView,
  ListView,
)

from .forms import BuildingForm, LeaseContractForm, UnitForm
from .models import Building, LeaseContract, Unit


# المباني
class BuildingListView(ListView):
  model = Building
  template_name = 'rentals/building_list.html'
  context_object_name = 'buildings'
  paginate_by = 10

def building_detail(request, pk):
  building = get_object_or_404(Building, pk=pk)
  return render(request, 'rentals/building_detail.html', {'building': building})

def building_update(request, pk):
  building = get_object_or_404(Building, pk=pk)
  if request.method == 'POST':
    form = BuildingForm(request.POST, instance=building)
    if form.is_valid():
      form.save()
      return redirect('building_detail', pk=building.pk)
  else:
    form = BuildingForm(instance=building)
  return render(request, 'rentals/building_form.html', {'form': form})

def building_delete(request, pk):
  building = get_object_or_404(Building, pk=pk)
  if request.method == 'POST':
    building.delete()
    return redirect('building_list')

class BuildingDetailView(DetailView):
  model = Building
  template_name = 'rentals/building_detail.html'

def building_create(request):
  if request.method == 'POST':
    form = BuildingForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('building_list')
  else:
    form = BuildingForm()
  return render(request, 'rentals/building_form.html', {'form': form})

# الوحدات
class UnitListView(ListView):
  model = Unit
  template_name = 'rentals/unit_list.html'
  #filterset_class = UnitFilter

def unit_detail(request, pk):
  unit = get_object_or_404(Unit, pk=pk)
  return render(request, 'rentals/unit_detail.html', {'unit': unit})

def unit_list(request):
  units = Unit.objects.all()
  return render(request, 'rentals/unit_list.html', {'units': units})

def unit_create(request):
  if request.method == 'POST':
    form = UnitForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('unit_list')
  else:
    form = UnitForm()
  return render(request, 'rentals/unit_form.html', {'form': form})

def unit_update(request, pk):
  unit = get_object_or_404(Unit, pk=pk)
  if request.method == 'POST':
    form = UnitForm(request.POST, instance=unit)
    if form.is_valid():
      form.save()
      return redirect('unit_detail', pk=unit.pk)
  else:
    form = UnitForm(instance=unit)
  return render(request, 'rentals/unit_form.html', {'form': form})

def unit_delete(request, pk):
  unit = get_object_or_404(Unit, pk=pk)
  if request.method == 'POST':
    unit.delete()
    return redirect('unit_list')

# العقود
def contract_list(request):
  contracts = LeaseContract.objects.all()
  return render(request, 'rentals/contract_list.html', {'contracts': contracts})

def contract_create(request):
  if request.method == 'POST':
    form = LeaseContractForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('contract_detail', pk=contract.pk)
  else:
    form = LeaseContractForm()
  return render(request, 'rentals/contract_form.html', {'form': form})

def contract_detail(request, pk):
  contract = get_object_or_404(LeaseContract, pk=pk)
  return render(request, 'rentals/contract_detail.html', {'contract': contract})

def contract_update(request, pk):
  contract = get_object_or_404(LeaseContract, pk=pk)
  if request.method == 'POST':
    form = LeaseContractForm(request.POST, request.FILES, instance=contract)
    if form.is_valid():
      form.save()
      return redirect('contract_detail', pk=contract.pk)
  else:
    form = LeaseContractForm(instance=contract)
  return render(request, 'rentals/contract_form.html', {'form': form})

def contract_renew(request, pk):
  contract = get_object_or_404(LeaseContract, pk=pk)
  if request.method == 'POST':
    form = LeaseContractForm(request.POST, request.FILES, instance=contract)
    if form.is_valid():
      form.save()
      return redirect('contract_detail', pk=contract.pk)
  else:
    form = LeaseContractForm(instance=contract)
  return render(request, 'rentals/contract_form.html', {'form': form})

def contract_terminate(request, pk):
  contract = get_object_or_404(LeaseContract, pk=pk)
  if request.method == 'POST':
    contract.delete()
    return redirect('contract_list')
  return render(request, 'rentals/contract_terminate.html', {'contract': contract})

def home(request):
  return render(request, 'rentals/home.html')