from django.contrib import admin
from .models import Vehicle


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('number', 'vehicle_type', 'slug', 'trolleys', 'warranty')
    list_filter = ('vehicle_type',)
    prepopulated_fields = {'slug': ('vehicle_type', 'number')}

admin.site.register(Vehicle, VehicleAdmin)

