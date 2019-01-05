from django.test import TestCase
from .models import Vehicle, Inspection, Complaint, Fault, Part
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

def create_fault(complaint, vehicle,zr_number='12345', category='silnik', status='open', description='test',
                 actions='actions',
                 comments='none'):
    fault = Fault.objects.create(complaint=complaint,
                                 vehicle=vehicle,
                                 zr_number=zr_number,
                                 category=category,
                                 status=status,
                                 description=description,
                                 actions=actions,
                                 comments=comments)
    return fault

def create_part(fault, name='przetwornica', index='1234', condition='new', origin='pesa'):
    part = Part.objects.create(fault=fault,
                               name=name,
                               index=index,
                               condition=condition,
                               origin=origin)
    return part


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
        vehicle = create_vehicle('001', 'SA132', 'sa132-001')
        create_inspection(vehicle=vehicle)

    def test_inspection_model(self):
        inspection = Inspection.objects.get(id=1)
        self.assertTrue(isinstance(inspection, Inspection))
        self.assertEqual(inspection.__str__(), 'Przegląd: P3.2, dzień wykonania: 12.9.2018')
        self.assertTrue(isinstance(inspection.vehicle, Vehicle))
        self.assertEqual(inspection.inspection_type, 'P3.2')


class ComplaintTestCase(TestCase):

    def setUp(self):
        vehicle = create_vehicle('003', 'SA132', 'sa132-003')
        user = User.objects.create_user('Tom')
        create_complaint(vehicle=vehicle, user=user)

    def test_complaint_model(self):
        vehicle = Vehicle.objects.get(id=1)
        user = User.objects.get(username='Tom')
        complaint = Complaint.objects.get(id=1)
        self.assertTrue(isinstance(complaint, Complaint))
        self.assertEqual(complaint.end_date, None)
        self.assertEqual(complaint.user, user)


class FautTestCase(TestCase):

    def setUp(self):
        vehicle = create_vehicle('001', 'SA132', 'sa132-001')
        user = User.objects.create_user('Tom')
        complaint = create_complaint(vehicle=vehicle, user=user)
        create_fault(complaint, vehicle)

    def test_fault_model(self):
        fault = Fault.objects.get(zr_number='12345')
        complaint = Complaint.objects.first()
        self.assertTrue(isinstance(fault, Fault))
        self.assertEqual(fault.zr_number, '12345')
        self.assertEqual(fault.end_date, None)
        self.assertEqual(fault.complaint, complaint)


class PartTestCase(TestCase):

    def setUp(self):
        vehicle = create_vehicle('001', 'SA132', 'sa132-001')
        user = User.objects.create_user('Tom')
        complaint = create_complaint(vehicle=vehicle, user=user)
        fault = create_fault(complaint, vehicle)
        create_part(fault=fault)

    def test_part_model(self):
        part = Part.objects.first()
        self.assertTrue(isinstance(part, Part))
        self.assertEqual(part.index, '1234')

