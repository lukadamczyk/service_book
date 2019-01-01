from django.contrib import admin
from .models import Vehicle, Inspection, Complaint


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('number', 'vehicle_type', 'slug', 'trolleys', 'warranty')
    list_filter = ('vehicle_type',)
    prepopulated_fields = {'slug': ('vehicle_type', 'number')}

admin.site.register(Vehicle, VehicleAdmin)


class InspectionAdmin(admin.ModelAdmin):
    list_display = ('date', 'inspection_type', 'performer', 'vehicle')
    list_filter = ('inspection_type', 'performer')

admin.site.register(Inspection, InspectionAdmin)

class ComplaintionAdmin(admin.ModelAdmin):
    list_display = ('document_number', 'vehicle', 'status', 'entry_date', 'tasks', 'updated', 'end_date', 'client',
                    'user')
    list_filter = ('vehicle', 'status')

admin.site.register(Complaint, ComplaintionAdmin)