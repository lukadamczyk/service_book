import datetime

from django.test import TestCase
from .forms import AddComplaintForm, EditComplaintForm, AddFaultForm, EditFaultForm
from .models import Vehicle, Trolleys, Owner
from .test_models import create_vehicle, create_owner, create_trolleys, create_complaint, create_fault


today = datetime.date.today()
day = datetime.timedelta(1)
yesterday = today - day
tomorrow = today + day

def create_form(doc, date, end_date, status, vehicle, form):
    data = {
        'document_number': doc,
        'entry_date': date,
        'end_date': end_date,
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

def create_edit_form(doc, entry_date, end_date, status, client, vehicle):
    data = {
        'document_number': doc,
        'entry_date': entry_date,
        'end_date': end_date,
        'status': status,
        'client': client,
        'vehicle': vehicle
    }
    edit_form = EditComplaintForm(data)
    return edit_form

def create_edit_fault_form(name, category, description, action, comments, zr, status, end_date, need):
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
    edit_form = EditFaultForm(data)
    return edit_form

class AddComplainFormTestCase(TestCase):
    def setUp(self):
        owner = create_owner()
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        create_vehicle(trolleys, owner, number='007', vehicle_type='SA132')

    def test_valid_form(self):
        vehicle = Vehicle.objects.get(number='007')
        test_form = create_form('Kw23', today, '', 'open', vehicle.id, AddComplaintForm)
        self.assertTrue(test_form.is_bound)
        self.assertTrue(test_form.is_valid())

    def test_invalid_form_document_number(self):
        vehicle = Vehicle.objects.get(number='007')
        test_form = create_form('', today, '', 'open', vehicle.id, AddComplaintForm)
        self.assertFalse(test_form.is_valid())

    def test_invalid_form_date(self):
        vehicle = Vehicle.objects.get(number='007')
        test_form = create_form('Kw23', yesterday, '', 'open', vehicle.id, AddComplaintForm)
        self.assertTrue(test_form.is_valid())
        test_form = create_form('Kw23', tomorrow, '', 'open', vehicle.id, AddComplaintForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors, {'__all__': ['Podaj właściwą datę rozpoczęcia reklamacji, nie może być pózniejsza niż '
                                            '{}'.format(datetime.date.today())]})

    def test_invalid_form_end_date(self):
        vehicle = Vehicle.objects.get(number='007')
        test_form = create_form('Kw23', today, yesterday, 'close', vehicle.id, AddComplaintForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors, {'__all__': ['Data zakończenia reklamacji nie moze być wcześniejsza niź '
                                                        'data rozpoczęcia']})

        test_form = create_form('Kw23', today, tomorrow, 'close', vehicle.id, AddComplaintForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors, {'__all__': ['Data zamknięcia reklamacji nie może być poźniejsza niż {}'.format(
            datetime.date.today())]})

    def test_invalid_form_end_date_and_open_status(self):
        vehicle = Vehicle.objects.get(number='007')
        test_form = create_form('Kw23', today, tomorrow, 'open', vehicle.id, AddComplaintForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors, {'__all__': ['Aby zamknąć rekalacje potrzeba wybrać zamknięty status '
                                                        'reklamacji i podać datę zakończenia']})

    def test_invalid_form_status_close_without_end_date(self):
        vehicle = Vehicle.objects.get(number='007')
        test_form = create_form('Kw23', today, '', 'close', vehicle.id, AddComplaintForm)
        self.assertTrue(test_form.is_bound)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors, {'__all__': ['Aby zamknąć rekalacje potrzeba wybrać zamknięty status '
                                                        'reklamacji i podać datę zakończenia']})

    def test_invalid_form_status(self):
        vehicle = Vehicle.objects.get(number='007')
        test_form = create_form('Kw23', yesterday, '', '', vehicle.id, AddComplaintForm)
        self.assertFalse(test_form.is_valid())
        test_form = create_form('Kw23', yesterday, '', 'text', vehicle.id, AddComplaintForm)
        self.assertFalse(test_form.is_valid())

    def test_invalid_form_vehicle(self):
        vehicle = Vehicle.objects.get(number='007')
        test_form = create_form('Kw23', yesterday, '', 'open', '', AddComplaintForm)
        self.assertFalse(test_form.is_valid())
        test_form = create_form('Kw23', yesterday, '', 'open', 3, AddComplaintForm)
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
        test_form = create_form_falut('', 'podłoga', 'test', '', '', '', 'open', '', '', AddFaultForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors,
                         {'name': ['To pole jest wymagane']})

        test_form = create_form_falut('asdfgqwertqwertqwertqwertqwertqw2wcfreota', 'podłoga', 'test', '', '', '',
                                      'open', '',
                                      '', AddFaultForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors,
                         {'name': ['To pole może zawierać maksymalinie 40 znaków']})


    def test_invalid_form_falut_category(self):
        test_form = create_form_falut('Kw12', '', 'test', '', '', '', 'open', '', '', AddFaultForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors,
                         {'category': ['To pole jest wymagane']})
        test_form = create_form_falut('Kw12', 'test', 'test', '', '', '', 'open', '', '', AddFaultForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors,
                         {'category': ['Wybierz jedną z proponowanych kategori']})

    def test_invalid_form_falut_description(self):
        test_form = create_form_falut('KW12', 'podłoga', '', '', '', '', 'open', '', '', AddFaultForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors,
                         {'description': ['To pole jest wymagane']})

    def test_invalid_form_zr(self):
        test_form = create_form_falut('usterka silnika', 'podłoga', 'test', '', '', '123421', 'open', '', '',
                                      AddFaultForm)
        self.assertTrue(test_form.is_valid())

        test_form = create_form_falut('usterka silnika', 'podłoga', 'test', '', '', '12344', 'open', '', '',
                                  AddFaultForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors,
                         {'__all__': ['Podaj właściwy numer ZR (6 cyfr)']})

        test_form = create_form_falut('usterka silnika', 'podłoga', 'test', '', '', '1234435', 'open', '', '',
                                      AddFaultForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors,
                         {'__all__': ['Podaj właściwy numer ZR (6 cyfr)']})

        test_form = create_form_falut('usterka silnika', 'podłoga', 'test', '', '', 'a34dc1', 'open', '', '',
                                      AddFaultForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors,
                         {'__all__': ['Podaj właściwy numer ZR (6 cyfr)']})

    def test_invalid_form_status(self):
        test_form = create_form_falut('usterka silnika', 'podłoga', 'test', '', '', '', '', '', '', AddFaultForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors,
                         {'status': ['To pole jest wymagane']})

    def test_invalid_form_end_date(self):
        test_form = create_form_falut('usterka silnika', 'podłoga', 'test', '', '', '', 'close', today, '',
                                      AddFaultForm)
        self.assertTrue(test_form.is_valid())

        test_form = create_form_falut('usterka silnika', 'podłoga', 'test', '', '', '', 'open', yesterday, '', AddFaultForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors,
                         {'__all__': ['Nie można podać daty zakończnia usterki przy otwarty statusie']})
        test_form = create_form_falut('usterka silnika', 'podłoga', 'test', '', '', '', 'close', '', '',
                                      AddFaultForm)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors,
                         {'__all__': ['Podaj datę zakończenia usterki']})


class EditComplaintFormTestCase(TestCase):
    def setUp(self):
        owner = create_owner()
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        create_vehicle(trolleys, owner, number='007', vehicle_type='SA132')

    def test_invalid_edit_complaint_document_number(self):
        client = Owner.objects.first()
        vehicle = Vehicle.objects.first()
        form = create_edit_form('', yesterday, today, 'close', client.id, vehicle.id)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'__all__': ['Wprowadź numer reklamacji']})

    def test_invalid_edit_complaint_entry_date(self):
        client = Owner.objects.first()
        vehicle = Vehicle.objects.first()
        form = create_edit_form('KW1234', tomorrow, today, 'close', client.id, vehicle.id)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'__all__': ['Data rozpoczęcia reklamacji nie może być późniejsza niż {}'.format(datetime.date.today())]})

        form = create_edit_form('KW1234', '', today, 'close', client.id, vehicle.id)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'__all__': ['Wprowadź datę rozpoczęcia reklamacji']})

    def test_invalid_edit_complaint_end_date(self):
        client = Owner.objects.first()
        vehicle = Vehicle.objects.first()
        form = create_edit_form('KW1234', today, yesterday, 'close', client.id, vehicle.id)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'__all__': ['Data zakończenia reklamacji nie może być wcześniejsza niż data '
                                                   'rozpoczęcia']})

        form = create_edit_form('KW1234', today, tomorrow, 'close', client.id, vehicle.id)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'__all__': ['Data zamknięcia reklamacji nie może być poźniejsza niż {}'.format(
            datetime.date.today())]})


class EditFaultFormTestCase(TestCase):
    def setUp(self):
        owner = create_owner()
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        vehicle = create_vehicle(trolleys, owner, '001', 'SA132', 'sa132-001')
        complaint = create_complaint(vehicle=vehicle, client=owner)

    def test_valid_edit_fault_form(self):
        form = create_edit_fault_form('fault', 'silnik', 'description', '', 'comments', '123456', 'open', '', '')
        self.assertTrue(form.is_valid())

    def test_invalid_edit_fault_zr(self):
        form = create_edit_fault_form('fault', 'silnik', 'description', '', 'comments', '12345', 'open', '', '')
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'__all__': ['Podaj właściwy numer ZR (6 cyfr)']})

    def test_invalid_edit_fault_form_status_close_without_end_date(self):
        form = create_edit_fault_form('fault', 'silnik', 'description', '', 'comments', '123456', 'close', '', '')
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'__all__': ['Podaj datę zakończenia usterki']})

    def test_invalid_edit_fault_form_status_open_with_end_date(self):
        form = create_edit_fault_form('fault', 'silnik', 'description', '', 'comments', '123456', 'open',
                                      datetime.date(2020, 4, 23), '')
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'__all__': ['Nie można podać daty zakończnia usterki przy otwarty statusie']})






