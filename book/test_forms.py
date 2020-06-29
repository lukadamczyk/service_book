import datetime

from django.test import TestCase
from .forms import AddComplaintForm, EditComplaintForm, AddFaultForm
from .models import Vehicle, Trolleys, Owner
from .test_models import create_vehicle, create_owner, create_trolleys, create_complaint, create_fault


today = datetime.date.today()
day = datetime.timedelta(1)
yesterday = today - day
tomorrow = today + day

def create_form(doc, date, status, vehicle, form):
    data = {
        'document_number': doc,
        'entry_date': date,
        'status': status,
        'vehicle': vehicle
    }
    add_form = form(data)
    return add_form

def create_form_falut(name, category, description, action, comments, zr, status, end_date, need, form):
    data = {
        'name': name,
        'category': category,
        'description': description,
        'actions': action,
        'comments': comments,
        'zr_number': zr,
        'status': status,
        'end_date': end_date,
        'need': need
    }
    fault_form = form(data)
    return fault_form

class AddComplainFormTestCase(TestCase):
    def setUp(self):
        owner = create_owner()
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        create_vehicle(trolleys, owner, number='007', vehicle_type='SA132')

    def test_valid_form(self):
        vehicle = Vehicle.objects.get(number='007')
        test_form = create_form('Kw23', today, 'open', vehicle.id, AddComplaintForm)
        self.assertTrue(test_form.is_bound)
        self.assertTrue(test_form.is_valid())

    def test_invalid_form_document_number(self):
        vehicle = Vehicle.objects.get(number='007')
        test_form = create_form('', today, 'open', vehicle.id, AddComplaintForm)
        self.assertFalse(test_form.is_valid())

    def test_invalid_form_date(self):
        vehicle = Vehicle.objects.get(number='007')
        test_form = create_form('Kw23', yesterday, 'open', vehicle.id, AddComplaintForm)
        self.assertTrue(test_form.is_valid())
        test_form = create_form('Kw23', tomorrow, 'open', vehicle.id, AddComplaintForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors, {'__all__': ['Podaj właściwą datę rozpoczęcia reklamacji, nie może być pózniejsza niż '
                                            '{}'.format(datetime.date.today())]})

    def test_invalid_form_status(self):
        vehicle = Vehicle.objects.get(number='007')
        test_form = create_form('Kw23', yesterday, '', vehicle.id, AddComplaintForm)
        self.assertFalse(test_form.is_valid())
        test_form = create_form('Kw23', yesterday, 'text', vehicle.id, AddComplaintForm)
        self.assertFalse(test_form.is_valid())

    def test_invalid_form_vehicle(self):
        vehicle = Vehicle.objects.get(number='007')
        test_form = create_form('Kw23', yesterday, 'open', '', AddComplaintForm)
        self.assertFalse(test_form.is_valid())
        test_form = create_form('Kw23', yesterday, 'open', 3, AddComplaintForm)
        self.assertFalse(test_form.is_valid())


class AddFaultFormTestCase(TestCase):
    def setUp(self):
        owner = create_owner()
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        vehicle = create_vehicle(trolleys, owner, '001', 'SA132', 'sa132-001')
        complaint = create_complaint(vehicle=vehicle, client=owner)

    def test_valid_form_fault(self):
        test_form = create_form_falut('usterka silnika', 'podłoga', 'test', '', '', '', 'open', '', '', AddFaultForm)
        self.assertTrue(test_form.is_valid())

    def test_invalid_form_falut_name(self):
        test_form = create_form_falut('kw123', 'podłoga', 'test', '', '', '', 'open', '', '', AddFaultForm)
        self.assertTrue(test_form.is_valid())

