from django.contrib import admin
from .models import Vehicle, Inspection


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('number', 'vehicle_type', 'slug', 'trolleys', 'warranty')
    list_filter = ('vehicle_type',)
    prepopulated_fields = {'slug': ('vehicle_type', 'number')}

admin.site.register(Vehicle, VehicleAdmin)


class InspectionAdmin(admin.ModelAdmin):
    list_display = ('date', 'inspection_type', 'performer', 'vehicle')
    list_filter = ('inspection_type', 'performer')

admin.site.register(Inspection, InspectionAdmin)