from django.contrib import admin

from rentals.models import Building, LeaseContract, Unit


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
  list_display = ('name', 'address', 'total_floors')
  list_filter = ('total_floors',)
  search_fields = ('name', 'address')
  
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
  list_display = ('unit_number', 'unit_type', 'building', 'monthly_rent', 'is_occupied')
  list_filter = ('unit_type', 'building', 'is_occupied')
  search_fields = ('unit_number', 'building__name')
  
@admin.register(LeaseContract)
class LeaseContractAdmin(admin.ModelAdmin):
  list_display = ('company', 'unit', 'start_date', 'end_date', 'monthly_rent')
  list_filter = ('start_date', 'end_date')
  search_fields = ('company__name', 'unit__unit_number')
  date_hierarchy = 'start_date'