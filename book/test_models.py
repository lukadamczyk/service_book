from django.test import TestCase
from .models import Vehicle, Inspection, Complaint, Fault
import datetime


def create_vehicle(number, vehicle_type, slug, trolleys, warranty):
    vehicle = Vehicle.objects.create(number=number,
                               vehicle_type=vehicle_type,
                               slug=slug,
                               trolleys=trolleys,
                               warranty=warranty)
    return vehicle

def create_inspection(date, vehicle, inspection_type, performer):
    inspection = Inspection.objects.create(date=date,
                            vehicle=vehicle,
                            inspection_type=inspection_type,
                            performer=performer)
    return inspection

class VehicleTestCase(TestCase):

    def setUp(self):
        create_vehicle(number='023',
                       vehicle_type='SA132',
                       slug='SA132-023',
                       trolleys='123453',
                       warranty=datetime.date(2018, 4, 12))

    def test_vehicle_model(self):
        vehicle = Vehicle.objects.get(id=1)
        self.assertEqual(vehicle.__str__(), 'Pojazd: SA132-023')
        self.assertEqual(vehicle.warranty, datetime.date(2018, 4, 12))
        self.assertTrue(isinstance(vehicle, Vehicle))
        self.assertEqual(vehicle.get_absolute_url(), '/vehicle/1/SA132-023')


class InspectionTestCase(TestCase):

    def setUp(self):
        vehicle = create_vehicle(number='023',
                       vehicle_type='SA132',
                       slug='SA132-023',
                       trolleys='123453',
                       warranty=datetime.date(2018, 4, 12))
        create_inspection(date=datetime.date(2018, 9, 12),
                          vehicle=vehicle,
                          inspection_type='P3.2',
                          performer='PESA')

    def test_inspection_model(self):
        inspection = Inspection.objects.get(id=1)
        self.assertTrue(isinstance(inspection, Inspection))
        self.assertEqual(inspection.__str__(), 'Przegląd: P3.2, dzień wykonania: 12.9.2018')
        self.assertTrue(isinstance(inspection.vehicle, Vehicle))
        self.assertEqual(inspection.inspection_type, 'P3.2')