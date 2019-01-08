from django.test import TestCase
from .models import Vehicle, Inspection, Complaint, Fault, Part, Owner, Trolleys
import datetime
from django.contrib.auth.models import User


def create_owner(name='KW', city='Poznań', address='ul.Kolejowa', slug='kw'):
    owner = Owner.objects.create(name=name,
                                 city=city,
                                 address=address,
                                 slug=slug)
    return owner

def create_trolleys(name, first, second):
    trolleys = Trolleys.objects.create(name=name,
                                       first=first,
                                        second=second)
    return trolleys

def create_vehicle(trolleys, owner, number='023', vehicle_type='SA132', slug='SA132-023', warranty=datetime.date(2018,
                                                                                                                4, 12)):
    vehicle = Vehicle.objects.create(number=number,
                                     vehicle_type=vehicle_type,
                                     slug=slug,
                                     trolleys=trolleys,
                                     warranty=warranty,
                                     owner=owner)
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

def create_complaint(vehicle, client, updated=None, doc_number='KW 123',
                     entry_date=datetime.date(2018, 2, 1), status='open',
                     tasks='test'):
    complaint = Complaint.objects.create(document_number=doc_number,
                                         entry_date=entry_date,
                                         updated=updated,
                                         status=status,
                                         tasks=tasks,
                                         client=client,
                                         vehicle=vehicle)
    return complaint

def create_fault(complaint, vehicle, name='usterka', zr_number='12345', category='silnik', status='open',
                 description='test',
                 actions='actions',
                 comments='none'):
    fault = Fault.objects.create(complaint=complaint,
                                 vehicle=vehicle,
                                 zr_number=zr_number,
                                 category=category,
                                 status=status,
                                 description=description,
                                 actions=actions,
                                 comments=comments,
                                 name=name)
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
        owner = create_owner()
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        create_vehicle(trolleys, owner)

    def test_vehicle_model(self):
        vehicle = Vehicle.objects.get(id=1)
        self.assertEqual(vehicle.__str__(), 'Pojazd: SA132-023')
        self.assertEqual(vehicle.warranty, datetime.date(2018, 4, 12))
        self.assertTrue(isinstance(vehicle, Vehicle))
        # self.assertEqual(vehicle.get_absolute_url(), '/vehicle/1/SA132-023')

    def test_get_full_name(self):
        vehicle = Vehicle.objects.get(id=1)
        self.assertEqual(vehicle.get_full_name(), 'SA132-023')


class InspectionTestCase(TestCase):

    def setUp(self):
        owner = create_owner()
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        vehicle = create_vehicle(trolleys, owner, '001', 'SA132', 'sa132-001')
        create_inspection(vehicle=vehicle)

    def test_inspection_model(self):
        inspection = Inspection.objects.get(id=1)
        self.assertTrue(isinstance(inspection, Inspection))
        self.assertEqual(inspection.__str__(), 'Przegląd: P3.2, dzień wykonania: 12.9.2018')
        self.assertTrue(isinstance(inspection.vehicle, Vehicle))
        self.assertEqual(inspection.inspection_type, 'P3.2')


class ComplaintTestCase(TestCase):

    def setUp(self):
        owner = create_owner()
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        vehicle = create_vehicle(trolleys, owner, '003', 'SA132', 'sa132-003')
        create_complaint(vehicle=vehicle, client=owner)

    def test_complaint_model(self):
        vehicle = Vehicle.objects.get(id=1)
        complaint = Complaint.objects.get(id=1)
        self.assertTrue(isinstance(complaint, Complaint))
        self.assertEqual(complaint.end_date, None)


class FautTestCase(TestCase):

    def setUp(self):
        owner = create_owner()
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        vehicle = create_vehicle(trolleys, owner, '001', 'SA132', 'sa132-001')
        complaint = create_complaint(vehicle=vehicle, client=owner)
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
        owner = create_owner()
        trolleys = create_trolleys(name='sa123', first='123', second='234')
        vehicle = create_vehicle(trolleys, owner, '001', 'SA132', 'sa132-001')
        complaint = create_complaint(vehicle=vehicle, client=owner)
        fault = create_fault(complaint, vehicle)
        create_part(fault=fault)

    def test_part_model(self):
        part = Part.objects.first()
        self.assertTrue(isinstance(part, Part))
        self.assertEqual(part.index, '1234')


class OwnerTestCase(TestCase):

    def setUp(self):
        create_owner()

    def test_owner_model(self):
        owner = Owner.objects.first()
        self.assertTrue(isinstance(owner, Owner))
        self.assertEqual(owner.name, 'KW')


class TrolleysTestCase(TestCase):

    def setUp(self):
        create_trolleys(name='sa123',first='123', second='234')

    def test_trolleys_model(self):
        trolleys = Trolleys.objects.first()
        self.assertTrue(isinstance(trolleys, Trolleys))
        self.assertEqual(trolleys.first, '123')
        self.assertEqual(trolleys.fifth, None)
