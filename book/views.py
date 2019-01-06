from django.shortcuts import render, get_object_or_404
from .models import Owner, Vehicle, Complaint


def home(request):
    owners = Owner.objects.all()
    return render(request,
                  template_name='book/index.html',
                  context={'title': 'Książka serwisowa',
                           'owners': owners})

def vehicle_list(request, slug):
    owner = get_object_or_404(Owner, slug=slug)
    return render(request,
                  template_name='book/vehicle/list.html',
                  context={'title': owner.name,
                           'owner': owner})

def vehicle_detail(request, slug):
    vehicle = get_object_or_404(Vehicle, slug=slug)
    title = '{}-{}'.format(vehicle.vehicle_type, vehicle.number)
    return render(request,
                  template_name='book/vehicle/detail.html',
                  context={'title': title,
                           'vehicle': vehicle})

def complaint_detail(request, id):
    complaint = get_object_or_404(Complaint, id=id)
    title = complaint.vehicle.get_full_name()
    return render(request,
                  template_name='book/complaint/detail.html',
                  context={'title': title,
                           'complaint': complaint})