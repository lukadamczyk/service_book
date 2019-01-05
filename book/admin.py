from django.contrib import admin
from .models import Vehicle, Inspection, Complaint, Fault, Part, Owner


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('number', 'vehicle_type', 'owner','slug', 'trolleys', 'warranty')
    list_filter = ('vehicle_type',)
    prepopulated_fields = {'slug': ('vehicle_type', 'number')}

admin.site.register(Vehicle, VehicleAdmin)


class InspectionAdmin(admin.ModelAdmin):
    list_display = ('date', 'inspection_type', 'performer', 'vehicle')
    list_filter = ('inspection_type', 'performer')

admin.site.register(Inspection, InspectionAdmin)

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('document_number', 'vehicle', 'status', 'entry_date', 'tasks', 'updated', 'end_date', 'client',
                    'user')
    list_filter = ('vehicle', 'status')

admin.site.register(Complaint, ComplaintAdmin)


class FaultAdmin(admin.ModelAdmin):
    list_display = ('name','zr_number', 'status', 'vehicle', 'description', 'actions', 'complaint', 'end_date',
                    'comments')
    list_filter = ('vehicle', 'status')

admin.site.register(Fault, FaultAdmin)


class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'index', 'fault', 'assembly_date', 'condition')
    list_filter = ('name', 'condition')

admin.site.register(Part, PartAdmin)


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address')

admin.site.register(Owner, OwnerAdmin)