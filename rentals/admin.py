from django.contrib import admin

from rentals.models import Building, LeaseContract, Unit

admin.site.register(Building)
admin.site.register(Unit)
admin.site.register(LeaseContract)