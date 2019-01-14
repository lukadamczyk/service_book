from django.shortcuts import render, get_object_or_404
from .models import Owner, Vehicle, Complaint, Fault, Inspection
from django.core.paginator import Paginator
from .forms import FilterComplaintsForm, FilterFaultForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import xlwt

def paginator_get_page(models_list, num, page):
    paginator = Paginator(models_list, num)
    return paginator.get_page(page)

@login_required()
def home(request):
    owners = Owner.objects.all()
    return render(request,
                  template_name='book/index.html',
                  context={'title': 'Książka serwisowa',
                           'owners': owners})

@login_required()
def vehicle_list(request, slug):
    owner = get_object_or_404(Owner, slug=slug)
    return render(request,
                  template_name='book/vehicle/list.html',
                  context={'title': owner.name,
                           'owner': owner})

@login_required()
def vehicle_detail(request, slug):
    vehicle = get_object_or_404(Vehicle, slug=slug)
    title = '{}-{}'.format(vehicle.vehicle_type, vehicle.number)
    return render(request,
                  template_name='book/vehicle/detail.html',
                  context={'title': title,
                           'vehicle': vehicle})

@login_required()
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
        complaints = paginator_get_page(complaints_list, 10, page)
        return render(request,
                      template_name='book/complaint/list.html',
                      context={'title': 'Reklamacje',
                               'complaints': complaints,
                               'form': form})
    complaints = paginator_get_page(complaints_list, 10, page)
    return render(request,
                  template_name='book/complaint/list.html',
                  context={'title': 'Reklamacje',
                           'complaints': complaints,
                           'form': form})

@login_required()
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

@login_required()
def fault_list(request):
    faults_list = Fault.objects.all()
    page = request.GET.get('page')
    form = FilterFaultForm(request.GET)
    if form.is_valid():
        cd = form.cleaned_data
        if cd['status']:
            faults_list = faults_list.filter(status=cd['status'])
        if cd['vehicle']:
            faults_list = faults_list.filter(vehicle=cd['vehicle'])
        if cd['zr_number']:
            faults_list = faults_list.filter(zr_number=cd['zr_number'])
        if cd['date_from']:
            faults_list = faults_list.filter(entry_date__gte=cd['date_from'])
        if cd['date_to']:
            faults_list = faults_list.filter(entry_date__lte=cd['date_to'])
        faults = paginator_get_page(faults_list, 10, page)
        return render(request,
                      template_name='book/fault/list.html',
                      context={'title': 'Usterki',
                               'faults': faults,
                               'form': form})
    faults = paginator_get_page(faults_list, 10, page)
    return render(request,
                  template_name='book/fault/list.html',
                  context={'title': 'Usterki',
                           'faults': faults,
                           'form': form})

@login_required()
def inspection_list(request):
    inspections = Inspection.objects.all()
    title = 'Przeglądy'
    return render(request,
                  template_name='book/inspection/list.html',
                  context={'title': title,
                           'inspections': inspections})

@login_required()
def inspection_detail(request, id):
    inspection = get_object_or_404(Inspection, id=id)
    title = 'Przegląd'
    return render(request,
                  template_name='book/inspection/detail.html',
                  context={'title': title,
                           'inspection': inspection})

@login_required()
def export_complaints_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=reklamacje.xls'

    def count_height(text):
        if len(text) > 25:
            lines = int(len(text) / 25) + 1
            return lines
        return 1

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Reklamcje')

    # Custom colors

    xlwt.add_palette_colour("light_green", 0x21)
    wb.set_colour_RGB(0x21, 184, 209, 175)
    xlwt.add_palette_colour("light_gray", 0x22)
    wb.set_colour_RGB(0x22, 227, 229, 229)

    # Sheet heade, first row
    row_num = 0

    font_style = xlwt.easyxf('align: vert centre, horiz centre, wrap on; font: bold on; borders: left thin, '
                             'right thin, top thin, bottom thin; pattern: pattern solid, fore_colour '
                                    'light_gray;')

    columns = ['Nr dokumentu', 'Pojazd', 'Data wejścia reklamacje', 'Data usunięcia reklamacji',
               'Status', 'Nr ZR', 'Usterka', 'Podjęte działania', 'Uwagi', 'Potrzeby']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # columns with
    ws.col(0).width = 256 * 25
    ws.col(1).width = 256 * 15
    ws.col(2).width = 256 * 15
    ws.col(3).width = 256 * 15
    ws.col(4).width = 256 * 15
    ws.col(5).width = 256 * 10
    ws.col(6).width = 256 * 40
    ws.col(7).width = 256 * 30
    ws.col(8).width = 256 * 30
    ws.col(9).width = 256 * 30

    ws.row(0).height = 256 * 3

    rows = Complaint.objects.all()

    for row in rows:
        row_num += 1
        for col_num in range(len(columns)):
            if row.status == 'open':
                style = xlwt.easyxf('align: vert centre, horiz centre, wrap yes; borders: left thin, right thin, '
                                    'top thin, bottom thin;')
            else:
                style = xlwt.easyxf('align: vert centre, horiz centre, wrap yes; pattern: pattern solid, fore_colour '
                                    'light_green; borders: left thin, right thin, top thin, bottom thin;')
            if col_num == 0:
                ws.write(row_num, col_num, row.document_number, style)
            if col_num == 1:
                ws.write(row_num, col_num, row.vehicle.get_full_name(), style)
            if col_num == 2:
                date = '-'.join((str(row.entry_date.day), str(row.entry_date.month), str(row.entry_date.year)))
                ws.write(row_num, col_num, date, style)
            if col_num == 3:
                if row.end_date:
                    date = '-'.join((str(row.end_date.day), str(row.end_date.month), str(row.end_date.year)))
                else:
                    date = ''
                ws.write(row_num, col_num, date, style)
            if col_num == 4:
                ws.write(row_num, col_num, row.status, style)
            if col_num == 5:
                faults = ''
                for i, fault in enumerate(row.complaint_faults.all()):
                    if fault.zr_number:
                        faults += '{}.{}\n'.format(i+1, fault.zr_number)
                ws.write(row_num, col_num, faults, style)
            if col_num == 6:
                faults = ''
                for i, fault in enumerate(row.complaint_faults.all()):
                    faults += '{}.{} - {}\n'.format(i+1, fault.description, fault.status)
                ws.row(row_num).height = 256 * count_height(faults)
                ws.write(row_num, col_num, faults, style)
            if col_num == 7:
                faults = ''
                for i, fault in enumerate(row.complaint_faults.all()):
                    if fault.actions:
                        faults += '{}.{}'.format(i + 1, fault.actions)
                ws.write(row_num, col_num, faults, style)
            if col_num == 8:
                faults = ''
                for i, fault in enumerate(row.complaint_faults.all()):
                    if fault.comments:
                        faults += '{}.{}'.format(i + 1, fault.comments)
                ws.write(row_num, col_num, faults, style)
            if col_num == 9:
                faults = ''
                for i, fault in enumerate(row.complaint_faults.all()):
                    if fault.need:
                        faults += '{}.{}'.format(i + 1, fault.need)
                ws.write(row_num, col_num, faults, style)
    ws.set_panes_frozen(True)
    ws.set_horz_split_pos(1)
    # ws.set_vert_split_pos(1)
    wb.save(response)
    return response