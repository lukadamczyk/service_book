from django.test import TestCase
from django.urls import reverse
from .test_models import create_vehicle, create_owner, create_trolleys, create_complaint, create_fault
from .models import Owner, Vehicle, Complaint, Fault
from django.contrib.auth.models import User

import datetime


class HomeViewTestcase(TestCase):

    def setUp(self):
        create_owner(name='Koleje Wielkopolskie')

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

    def test_vehicle_list_view(self):
        owner = Owner.objects.get(id=1)
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
        create_complaint(vehicle, owner, doc_number='reklamacja 34', entry_date=datetime.date(2019, 1, 12))

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

class FaultDetailViewTestCase(TestCase):

    def setUp(self):
        owner = create_owner(name='Koleje Dolnośląskie', slug='koleje-dolnośląskie')
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        vehicle = create_vehicle(trolleys, owner, slug='SA132-004', number='004', vehicle_type='SA132')
        complaint = create_complaint(vehicle, owner, doc_number='reklamacja 32')
        create_fault(complaint, vehicle, name='usterka drzwi')
        create_fault(complaint, vehicle, name='usterka silnika', zr_number='234')

    def test_fault_detail_view(self):
        fault = Fault.objects.get(id=1)
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
        complaint2 = create_complaint(vehicle2, owner, doc_number='reklamacja 32')
        complaint3 = create_complaint(vehicle3, owner, doc_number='reklamacja 32')
        create_fault(complaint1, vehicle1, name='usterka drzwi', entry_date=datetime.date(2019,1,2))
        create_fault(complaint2, vehicle2, name='usterka WC', zr_number='234', entry_date=datetime.date(2019,1,1))
        create_fault(complaint3, vehicle3, name='usterka silnika', zr_number='214', entry_date=datetime.date(2019,1,10))

    def test_fault_list_view(self):
        response = self.client.get(reverse('book:fault_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/fault/list.html')
        self.assertEqual(response.context['title'], 'Usterki')
        self.assertQuerysetEqual(response.context['faults'], ['<Fault: usterka WC>',
                                                      '<Fault: usterka drzwi>',
                                                      '<Fault: usterka silnika>'])
        self.assertContains(response, 'usterka drzwi')