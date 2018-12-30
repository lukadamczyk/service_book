from django.test import TestCase
from .models import Vehicle, Inspection, Complaint, Fault
import datetime


class VehicleTestCase(TestCase):

    def setUp(self):
        Vehicle.objects.create(number='023',
                               vehicle_type='SA132',
                               slug='SA132-023',
                               trolleys='123453',
                               warranty=datetime.date(2018, 4, 12))

    def test_str_represntation(self):
        vehicle = Vehicle.objects.get(id=1)
        self.assertEqual(vehicle.__str__(), 'Pojazd: SA132-023')
        self.assertEqual(vehicle.warranty, datetime.date(2018, 4, 12))
        self.assertTrue(isinstance(vehicle, Vehicle))
        self.assertEqual(vehicle.get_absolute_url(), '/vehicle/1/SA132-023')