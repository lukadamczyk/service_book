from django.shortcuts import render, get_object_or_404
from .models import Owner


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