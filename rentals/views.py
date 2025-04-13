from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Building, Unit, LeaseContract
from .forms import BuildingForm, UnitForm, LeaseContractForm

# المباني
class BuildingListView(ListView):
  model = Building
  template_name = 'rentals/building_list.html'
  context_object_name = 'buildings'
  paginate_by = 10

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
  filterset_class = UnitFilter

def unit_detail(request, pk):
  unit = get_object_or_404(Unit, pk=pk)
  return render(request, 'rentals/unit_detail.html', {'unit': unit})

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