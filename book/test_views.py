from django.test import TestCase
from django.urls import reverse
from .test_models import create_vehicle, create_owner, create_trolleys, create_complaint
from .models import Owner, Vehicle, Complaint
from django.contrib.auth.models import User


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
        user = User.objects.create_user('Tom')
        create_complaint(vehicle, user, owner, doc_number='reklamacja 32')

    def test_complaint_detail_view(self):
        complaint = Complaint.objects.first()
        response = self.client.get(reverse('book:complaint_detail', args=[complaint.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/complaint/detail.html')
        self.assertEqual(response.context['title'], 'SA132-001')
        self.assertEqual(response.context['complaint'], complaint)
        self.assertContains(response, 'reklamacja 32')
