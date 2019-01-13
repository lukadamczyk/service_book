from django.shortcuts import render, get_object_or_404
from .models import Owner, Vehicle, Complaint, Fault, Inspection
from django.core.paginator import Paginator
from .forms import FilterComplaintsForm
from django.db.models import Q


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

def complaint_list(request):
    complaints_list = Complaint.objects.all()
    page = request.GET.get('page')
    form = FilterComplaintsForm(request.GET)
    if form.is_valid():
        cd = form.cleaned_data
        if cd['status']:
            complaints_list = complaints_list.filter(status=cd['status'])
        if cd['vehicle']:
            complaints_list = complaints_list.filter(vehicle=cd['vehicle'])
        if cd['date_from']:
            complaints_list = complaints_list.filter(entry_date__gte=cd['date_from'])
        if cd['date_to']:
            complaints_list = complaints_list.filter(entry_date__lte=cd['date_to'])
        paginator = Paginator(complaints_list, 10)
        complaints = paginator.get_page(page)
        return render(request,
                      template_name='book/complaint/list.html',
                      context={'title': 'Reklamacje',
                               'complaints': complaints,
                               'form': form})
    paginator = Paginator(complaints_list, 10)
    complaints = paginator.get_page(page)
    return render(request,
                  template_name='book/complaint/list.html',
                  context={'title': 'Reklamacje',
                           'complaints': complaints,
                           'form': form})

def complaint_detail(request, id):
    complaint = get_object_or_404(Complaint, id=id)
    title = complaint.vehicle.get_full_name()
    return render(request,
                  template_name='book/complaint/detail.html',
                  context={'title': title,
                           'complaint': complaint})

def fault_detail(request, id):
    fault = get_object_or_404(Fault, id=id)
    title = fault.vehicle.get_full_name()
    return render(request,
                  template_name='book/fault/detail.html',
                  context={'title': title,
                           'fault': fault})

def fault_list(request):
    faults = Fault.objects.all()
    title = 'Usterki'
    return render(request,
                  template_name='book/fault/list.html',
                  context={'title': title,
                           'faults': faults})

def inspection_list(request):
    inspections = Inspection.objects.all()
    title = 'Przeglądy'
    return render(request,
                  template_name='book/inspection/list.html',
                  context={'title': title,
                           'inspections': inspections})

def inspection_detail(request, id):
    inspection = get_object_or_404(Inspection, id=id)
    title = 'Przegląd'
    return render(request,
                  template_name='book/inspection/detail.html',
                  context={'title': title,
                           'inspection': inspection})