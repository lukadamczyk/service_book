from django.test import TestCase
from .models import Vehicle, Inspection, Complaint, Fault
import datetime
from django.contrib.auth.models import User


def create_vehicle(number='023', vehicle_type='SA132', slug='SA132-023', trolleys='123453', warranty=datetime.date(2018, 4, 12)):
    vehicle = Vehicle.objects.create(number=number,
                               vehicle_type=vehicle_type,
                               slug=slug,
                               trolleys=trolleys,
                               warranty=warranty)
    return vehicle

def create_inspection(vehicle, date=datetime.date(2018, 9, 12), inspection_type='P3.2',
                      performer='PESA'):
    inspection = Inspection.objects.create(date=date,
                            vehicle=vehicle,
                            inspection_type=inspection_type,
                            performer=performer)
    return inspection

def create_user(username, email='john@gmail.com', password='password'):
    user = User.objects.create_user(username=username,
                                    email=email,
                                    password=password)
    return user

def create_complaint(vehicle, user, updated=None, doc_number='KW 123',
                     entry_date=datetime.datetime(2018, 2, 1),
                     status='open',
                     tasks='test',
                     client='KW'):
    complaint = Complaint.objects.create(document_number=doc_number,
                                         entry_date=entry_date,
                                         updated=updated,
                                         status=status,
                                         tasks=tasks,
                                         client=client,
                                         vehicle=vehicle,
                                         user=user)
    return complaint

class VehicleTestCase(TestCase):

    def setUp(self):
        create_vehicle()

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