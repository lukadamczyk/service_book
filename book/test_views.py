from django.test import TestCase
from django.urls import reverse
from .test_models import create_vehicle, create_owner, create_trolleys, create_complaint, create_fault, create_inspection
from .models import Owner, Vehicle, Complaint, Fault, Inspection
from django.contrib.auth.models import User
from .forms import FilterComplaintsForm, FilterFaultForm


import datetime


class HomeViewTestcase(TestCase):

    def setUp(self):
        create_owner(name='Koleje Wielkopolskie')
        User.objects.create_user('Tom',
                                 'tom@mail.com',
                                 'tompassword')
        self.client.login(username='Tom',
                          password='tompassword')

    def test_home_view(self):
        response = self.client.get(reverse('book:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/index.html')
        self.assertEqual(response.context['title'], 'Książka serwisowa')
        self.assertQuerysetEqual(response.context['owners'], ['<Owner: Koleje Wielkopolskie>'])
        self.assertContains(response, 'Koleje Wielkopolskie')


class VehicleListViewTestCase(TestCase):

    def setUp(self):
        owner = create_owner(name='Koleje Dolnośląskie', slug='koleje-dolnośląskie')
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        create_vehicle(trolleys, owner, slug='SA132-001', number='001', vehicle_type='SA132')
        User.objects.create_user('Tom',
                                 'tom@mail.com',
                                 'tompassword')
        self.client.login(username='Tom',
                          password='tompassword')

    def test_vehicle_list_view(self):
        owner = Owner.objects.get(name='Koleje Dolnośląskie')
        response = self.client.get(reverse('book:vehicle_list', args=['koleje-dolnośląskie']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/vehicle/list.html')
        self.assertEqual(response.context['title'], 'Koleje Dolnośląskie')
        self.assertEqual(response.context['owner'], owner)
        self.assertContains(response, 'Pojazd: SA132-001')


class VehicleDetailViewTestCase(TestCase):

    def setUp(self):
        owner = create_owner(name='Koleje Dolnośląskie', slug='koleje-dolnośląskie')
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        create_vehicle(trolleys, owner, slug='SA132-001', number='001', vehicle_type='SA132')
        User.objects.create_user('Tom',
                                 'tom@mail.com',
                                 'tompassword')
        self.client.login(username='Tom',
                          password='tompassword')

    def test_vehicle_detail_view(self):
        vehicle = Vehicle.objects.first()
        response = self.client.get(reverse('book:vehicle_detail', args=[vehicle.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/vehicle/detail.html')
        self.assertEqual(response.context['title'], 'SA132-001')
        self.assertEqual(response.context['vehicle'], vehicle)
        self.assertContains(response, 'Pojazd: SA132-001')



class ComplaintDetailViewTestCase(TestCase):

    def setUp(self):
        owner = create_owner(name='Koleje Dolnośląskie', slug='koleje-dolnośląskie')
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        vehicle = create_vehicle(trolleys, owner, slug='SA132-001', number='001', vehicle_type='SA132')
        create_complaint(vehicle, owner, doc_number='reklamacja 32')
        User.objects.create_user('Tom',
                                 'tom@mail.com',
                                 'tompassword')
        self.client.login(username='Tom',
                          password='tompassword')

    def test_complaint_detail_view(self):
        complaint = Complaint.objects.first()
        response = self.client.get(reverse('book:complaint_detail', args=[complaint.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/complaint/detail.html')
        self.assertEqual(response.context['title'], 'SA132-001')
        self.assertEqual(response.context['complaint'], complaint)
        self.assertContains(response, 'reklamacja 32')


class ComplaintListViewTestCase(TestCase):

    def setUp(self):
        owner = create_owner(name='Koleje Dolnośląskie', slug='koleje-dolnośląskie')
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        vehicle = create_vehicle(trolleys, owner, slug='SA132-001', number='001', vehicle_type='SA132')
        create_complaint(vehicle, owner, doc_number='reklamacja 32', entry_date=datetime.date(2019, 1, 1))
        create_complaint(vehicle, owner, doc_number='reklamacja 33', entry_date=datetime.date(2019, 1, 3))
        create_complaint(vehicle, owner, doc_number='reklamacja 34', entry_date=datetime.date(2019, 1, 12),
                         status='close')
        User.objects.create_user('Tom',
                                 'tom@mail.com',
                                 'tompassword')
        self.client.login(username='Tom',
                          password='tompassword')

    def test_complaint_list_view(self):
        complaints = Complaint.objects.all()
        response = self.client.get(reverse('book:complaint_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/complaint/list.html')
        self.assertEqual(response.context['title'], 'Reklamacje')
        self.assertQuerysetEqual(response.context['complaints'],  ['<Complaint: reklamacja 34>',
                                                                   '<Complaint: reklamacja 33>',
                                                                   '<Complaint: reklamacja 32>'])
        self.assertEqual(len(response.context['complaints']), 3)
        self.assertContains(response, 'reklamacja 33')

    def test_valid_form(self):
        vehicle = Vehicle.objects.first()
        form = FilterComplaintsForm(data={'status': 'open',
                                          'vehicle': vehicle.id})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = FilterComplaintsForm(data={'status': 'op'})
        self.assertFalse(form.is_valid())

    def test_serch_by_status(self):
        response = self.client.get('/complaint/?status=open&vehicle=')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['complaints']), 2)

    def test_search_by_date(self):
        response = self.client.get('/complaint/?status=&vehicle=&date_from=2019-1-1&date_to=2019-1-3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['complaints']), 2)


class FaultDetailViewTestCase(TestCase):

    def setUp(self):
        owner = create_owner(name='Koleje Dolnośląskie', slug='koleje-dolnośląskie')
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        vehicle = create_vehicle(trolleys, owner, slug='SA132-004', number='004', vehicle_type='SA132')
        complaint = create_complaint(vehicle, owner, doc_number='reklamacja 35')
        create_fault(complaint, vehicle, name='usterka drzwi')
        create_fault(complaint, vehicle, name='usterka silnika', zr_number='234')
        User.objects.create_user('Tom',
                                 'tom@mail.com',
                                 'tompassword')
        self.client.login(username='Tom',
                          password='tompassword')

    def test_fault_detail_view(self):
        fault = Fault.objects.get(name='usterka drzwi')
        response = self.client.get(reverse('book:fault_detail', args=[fault.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/fault/detail.html')
        self.assertEqual(response.context['title'], 'SA132-004')
        self.assertEqual(response.context['fault'], fault)
        self.assertContains(response, 'Usterka: usterka drzwi')


class FaultListViewTestCase(TestCase):

    def setUp(self):
        owner = create_owner(name='Koleje Dolnośląskie', slug='koleje-dolnośląskie')
        trolleys1 = create_trolleys(name='sa123', first='123', second='2334')
        trolleys2 = create_trolleys(name='sa1232', first='13', second='2324')
        trolleys3 = create_trolleys(name='sa1233', first='1213', second='2134')
        vehicle1 = create_vehicle(trolleys1, owner, slug='SA132-004', number='004', vehicle_type='SA132')
        vehicle2 = create_vehicle(trolleys2, owner, slug='SA132-020', number='020', vehicle_type='SA132')
        vehicle3 = create_vehicle(trolleys3, owner, slug='SA132-001', number='001', vehicle_type='SA132')
        complaint1 = create_complaint(vehicle1, owner, doc_number='reklamacja 32')
        complaint2 = create_complaint(vehicle2, owner, doc_number='reklamacja 33')
        complaint3 = create_complaint(vehicle3, owner, doc_number='reklamacja 34')
        create_fault(complaint1, vehicle1, name='usterka drzwi', entry_date=datetime.date(2019,1,2), status='close')
        create_fault(complaint2, vehicle2, name='usterka WC', zr_number='234', entry_date=datetime.date(2019,1,1))
        create_fault(complaint3, vehicle3, name='usterka silnika', zr_number='214', entry_date=datetime.date(2019,1,10))
        User.objects.create_user('Tom',
                                 'tom@mail.com',
                                 'tompassword')
        self.client.login(username='Tom',
                          password='tompassword')

    def test_fault_list_view(self):
        response = self.client.get(reverse('book:fault_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/fault/list.html')
        self.assertEqual(response.context['title'], 'Usterki')
        self.assertQuerysetEqual(response.context['faults'], ['<Fault: usterka WC>',
                                                      '<Fault: usterka drzwi>',
                                                      '<Fault: usterka silnika>'])
        self.assertContains(response, 'usterka drzwi')

    def test_valid_form(self):
        form_blank = FilterFaultForm(data={})
        form_data = FilterFaultForm(data={'status': 'open'})
        self.assertTrue(form_blank.is_valid())
        self.assertTrue(form_data.is_valid())

    def test_invalid_form(self):
        form_data = FilterFaultForm(data={'status': 'test'})
        self.assertFalse(form_data.is_valid())

    def test_serch_by_status(self):
        response = self.client.get('/fault/?status=open&vehicle=')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['faults']), 2)

    def test_search_by_date(self):
        response = self.client.get('/fault/?status=&vehicle=&date_from=2019-1-1&date_to=2019-1-3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['faults']), 2)


class InspectionListViewTestCase(TestCase):

    def setUp(self):
        owner = create_owner(name='Koleje Dolnośląskie', slug='koleje-dolnośląskie')
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        vehicle = create_vehicle(trolleys, owner, slug='SA132-001', number='001', vehicle_type='SA132')
        create_inspection(vehicle, date=datetime.date(2019, 1, 2), inspection_type='P1.1')
        create_inspection(vehicle, date=datetime.date(2019, 1, 1), inspection_type='P2.1')
        create_inspection(vehicle, date=datetime.date(2019, 1, 12), inspection_type='P1.3')
        User.objects.create_user('Tom',
                                 'tom@mail.com',
                                 'tompassword')
        self.client.login(username='Tom',
                          password='tompassword')

    def test_inspection_list_view(self):
        response = self.client.get(reverse('book:inspection_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/inspection/list.html')
        self.assertEqual(response.context['title'], 'Przeglądy')
        self.assertQuerysetEqual(response.context['inspections'], ['<Inspection: Przegląd: P1.3, dzień wykonania: '
                                                                   '12.1.2019>',
                                                                   '<Inspection: Przegląd: P1.1, dzień wykonania: '
                                                                   '2.1.2019>',
                                                                   '<Inspection: Przegląd: P2.1, dzień wykonania: '
                                                                   '1.1.2019>'])
        self.assertContains(response, 'P2.1')


class InspectionDetailViewTestCase(TestCase):

    def setUp(self):
        owner = create_owner(name='Koleje Dolnośląskie', slug='koleje-dolnośląskie')
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        vehicle = create_vehicle(trolleys, owner, slug='SA132-001', number='001', vehicle_type='SA132')
        create_inspection(vehicle, date=datetime.date(2019, 1, 2), inspection_type='P1.1')
        create_inspection(vehicle, date=datetime.date(2019, 1, 1), inspection_type='P2.1')
        create_inspection(vehicle, date=datetime.date(2019, 1, 12), inspection_type='P1.3')
        User.objects.create_user('Tom',
                                 'tom@mail.com',
                                 'tompassword')
        self.client.login(username='Tom',
                          password='tompassword')

    def test_inspection_detail_view(self):
        inspection = Inspection.objects.get(id=2)
        response = self.client.get(reverse('book:inspection_detail', args=[inspection.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/inspection/detail.html')
        self.assertEqual(response.context['title'], 'Przegląd')
        self.assertEqual(response.context['inspection'], inspection)
        self.assertContains(response, 'P1.1')


class AddComplaintView(TestCase):

    def setUp(self):
        User.objects.create_user('Tom',
                                 'tom@mail.com',
                                 'tompassword')
        self.client.login(username='Tom',
                          password='tompassword')
        client = create_owner(name='Koleje Dolnośląskie', slug='koleje-dolnośląskie')
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        create_vehicle(trolleys, client, slug='SA132-001', number='001', vehicle_type='SA132')

    def test_valid_add_complaint(self):
        client = Owner.objects.first()
        vehicle = Vehicle.objects.first()
        data = {'document_number': 'KW1234',
                'entry_date': datetime.date(2019, 1, 1),
                'status': 'open',
                'vehicle': vehicle.id,
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-name': 'usterka drzwi',
                'form-0-category': 'poszycie',
                'form-0-zr_number': '121234',
                'form-0-status': 'close',
                'form-0-description': 'uszkodzony sterownik drzwi',
                'form-0-end_date': datetime.date(2019, 1, 1)}
        response = self.client.post('/complaint/add/?number={}'.format(vehicle.id),
                                    data=data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/complaint/list.html')
        complaint = Complaint.objects.get(document_number='KW1234')
        self.assertEqual(complaint.entry_date, datetime.date(2019, 1, 1))
        self.assertEqual(len(complaint.complaint_faults.all()), 1)
        fault = Fault.objects.get(complaint=complaint)
        self.assertEqual(fault.zr_number, '121234')
        self.assertEqual(fault.entry_date, complaint.entry_date)

    def test_invaild_add_fault_close_without_end_date(self):
        client = Owner.objects.first()
        vehicle = Vehicle.objects.first()
        data = {'document_number': 'KW12322',
                'entry_date': datetime.date(2019, 1, 1),
                'status': 'open',
                'vehicle': vehicle.id,
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-name': 'usterka drzwi',
                'form-0-category': 'poszycie',
                'form-0-zr_number': '123123',
                'form-0-status': 'close',
                'form-0-description': 'uszkodzony sterownik drzwi',
                'form-0-end_date': ''}
        response = self.client.post('/complaint/add/?number={}'.format(vehicle.id),
                                    data=data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/complaint/add.html')
        complaints = Complaint.objects.all()
        self.assertEqual(len(complaints), 0)
        self.assertContains(response, 'Podaj datę zakończenia')

    def test_invaild_add_fault_wrong_end_date(self):
        client = Owner.objects.first()
        vehicle = Vehicle.objects.first()
        data = {'document_number': 'KW1234',
                'entry_date': datetime.date(2019, 1, 12),
                'status': 'open',
                'vehicle': vehicle.id,
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-name': 'usterka drzwi',
                'form-0-category': 'poszycie',
                'form-0-zr_number': '123123',
                'form-0-status': 'close',
                'form-0-description': 'uszkodzony sterownik drzwi',
                'form-0-end_date': datetime.date(2019, 1, 1)}
        response = self.client.post('/complaint/add/?number=1',
                                    data=data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/complaint/add.html')
        complaints = Complaint.objects.all()
        self.assertEqual(len(complaints), 0)
        self.assertContains(response, 'Data zakończenia usterki nie może być wcześniejsza niż data '
                                           'wpłynięcia reklamacji')


