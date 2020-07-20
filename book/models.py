from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

import datetime, os

vehicle_choices = (
        ('SA132', 'SA132'),
        ('SA133', 'SA133'),
        ('SA134', 'SA134'),
        ('SA136', 'SA136'),
        ('SA139', 'SA139'),
)


def user_directory_path(instance, file_name):
    return 'complaint_{0}/{1}'.format(instance.complaint.id, file_name)


class Owner(models.Model):
    name = models.CharField(max_length=20,
                            unique=True)
    slug = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @property
    def create_image_path(self):
        img_path = 'book/{}.jpeg'.format(self.name)
        return img_path

class Trolleys(models.Model):
    name = models.CharField(max_length=10,
                            unique=True)
    first = models.CharField(max_length=20,
                             unique=True)
    second = models.CharField(max_length=20,
                              unique=True)
    third = models.CharField(max_length=20,
                             blank=True,
                             unique=True,
                             null=True)
    fourth = models.CharField(max_length=20,
                              blank=True,
                              unique=True,
                              null=True)
    fifth = models.CharField(max_length=20,
                             blank=True,
                             unique=True,
                             null=True)
    sixth = models.CharField(max_length=20,
                             blank=True,
                             unique=True,
                             null=True)
    seventh = models.CharField(max_length=20,
                               blank=True,
                               unique=True,
                               null=True)
    eighth = models.CharField(max_length=20,
                              blank=True,
                              unique=True,
                              null=True)
    ninth = models.CharField(max_length=20,
                             blank=True,
                             unique=True,
                             null=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    number = models.CharField(max_length=10)
    vehicle_type = models.CharField(max_length=10,
                                    db_index=True,
                                    choices=vehicle_choices)
    slug = models.SlugField(max_length=20,
                            db_index=True,
                            unique=True)
    trolleys = models.OneToOneField(Trolleys,
                                 related_name='vehicle_trolleys',
                                 on_delete=models.CASCADE)
    warranty = models.DateField()
    owner = models.ForeignKey(Owner,
                              related_name='owners',
                              on_delete=models.CASCADE,
                              db_index=True)

    class Meta:
        ordering = ('vehicle_type', 'number')

    def __str__(self):
        return 'Pojazd: {}-{}'.format(self.vehicle_type, self.number)

    @property
    def get_full_name(self):
        return '{}-{}'.format(self.vehicle_type, self.number)

    def is_warrenty(self, date=None):
        if date:
            today = date
        else:
            today = datetime.date.today()
        if self.warranty >= today:
            return True
        else:
            return False

    # def get_absolute_url(self):
    #     return reverse('book:vehicle_detail',
    #                    args=[self.id, self.slug])


class Inspection(models.Model):
    choices = (
        ('P1.1', 'P1.1'),
        ('P1.2', 'P1.2'),
        ('P1.3', 'P1.3'),
        ('P2.1', 'P2.1'),
        ('P2.2', 'P2.2'),
        ('P2.3', 'P2.3'),
        ('P3.1', 'P3.1'),
        ('P3.2', 'P3.2'),
    )
    date = models.DateField()
    inspection_type = models.CharField(max_length=10,
                                       db_index=True,
                                       choices=choices)
    performer = models.CharField(max_length=30,
                                 db_index=True)
    vehicle = models.ForeignKey(Vehicle,
                                related_name='vehicles',
                                on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return 'Przegląd: {}, dzień wykonania: {}.{}.{}'.format(self.inspection_type, self.date.day, self.date.month,
                                                                self.date.year)


class Complaint(models.Model):
    status_choices = (
        ('open', 'Otwarta'),
        ('close', 'Zamknięta')
    )
    published_date = models.DateTimeField(auto_now_add=True)
    document_number = models.CharField(max_length=50,
                                       unique=True)
    entry_date = models.DateField()
    updated = models.DateField(auto_now=True)
    end_date = models.DateField(blank=True,
                                    null=True)
    status = models.CharField(max_length=10,
                              choices=status_choices)
    tasks = models.TextField(blank=True,
                             null=True)
    client = models.ForeignKey(Owner,
                               related_name='owners_complaint',
                               on_delete=models.CASCADE,
                               db_index=True)
    vehicle = models.ForeignKey(Vehicle,
                                related_name='complaint_vehicles',
                                on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               related_name='auth_complaint',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)

    def __str__(self):
        return self.document_number

    class Meta:
        ordering = ('-entry_date',)

    @property
    def day_counter(self):
        days = datetime.date.today() - self.entry_date
        return days.days


class File(models.Model):
    complaint = models.ForeignKey(Complaint,
                                  related_name='files_complaint',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    file_document = models.FileField(upload_to=user_directory_path,
                            blank=True,
                            null=True)

    @property
    def get_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.file_document.url)


class Fault(models.Model):
    status_choices = (
        ('open', 'Otwarta'),
        ('close', 'Zamknięta')
    )
    category_choices = (
        ('pudło', (
            ('nadwozie', 'Nadwozie'),
            ('poszycie', 'Poszycie'),
            ('podłoga', 'Podłoga'),
            ('konstrukcja', 'Konstrukcja'),
            ('układy nośne', 'Układy nośne'),
            ('grodzenia', 'Grodzenia'),
        )),
        ('materiały wykończeniowe', (
            ('malatura', 'Malatura'),
            ('kalkomania', 'Kalkomania'),
        )),
        ('wyposażnie wewn.', 'Wyposażenie wewnętrzne'),
        ('wózek', 'Wózek'),
        ('urządz. ster. pojazdem', 'Urządzenia sterujące pojazdem'),
        ('urządz, monitoringu i bezpiecz.', 'Urządzenia monitoringu i bezpieczeństwa'),
        ('klima i orzewanie', 'Klimatyzacja i ogrzewanie'),
        ('drzwi', 'Drzwi'),
        ('sip', 'Urządzenia informacyjne'),
        ('układ hamowania', 'Układ hamowania'),
        ('układ sprzęgania', 'Układ sprzęgania'),
        ('okna i szyby', 'Okna i szyby'),
        ('układ elek.', 'Układ elektryczny'),
        ('Układ napędowy', (
            ('silnik', 'Silnik'),
            ('przekładnia', 'Przekładnia'),
        )),
        ('Wyposażenie zewnętrzne', (
            ('wycieraczki', 'Wycieraczki'),
            ('lusterka', 'Lusterka'),
            ('syreny', 'Syreny'),
        )),
        ('układ pneumatyczny', 'Układ pneumatyczny'),
    )
    name = models.CharField(max_length=40)
    category = models.CharField(max_length=50,
                                db_index=True,
                                choices=category_choices)
    description = models.TextField()
    actions = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    zr_number = models.CharField(max_length=10,
                                 unique=True,
                                 blank=True,
                                 null=True)
    status = models.CharField(max_length=10,
                              choices=status_choices)
    entry_date = models.DateField()
    end_date = models.DateField(blank=True,
                                null=True)
    need = models.TextField(blank=True)
    complaint = models.ForeignKey(Complaint,
                                  related_name='complaint_faults',
                                  on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle,
                                related_name='vehicle_faults',
                                on_delete=models.CASCADE)

    class Meta:
        ordering = ('-entry_date',)

    def __str__(self):
        return self.name


class Fault_without_complaint(models.Model):
    status_choices = (
        ('open', 'Otwarta'),
        ('close', 'Zamknięta')
    )
    category_choices = (
        ('pudło', (
            ('nadwozie', 'Nadwozie'),
            ('poszycie', 'Poszycie'),
            ('podłoga', 'Podłoga'),
            ('konstrukcja', 'Konstrukcja'),
            ('układy nośne', 'Układy nośne'),
            ('grodzenia', 'Grodzenia'),
        )),
        ('materiały wykończeniowe', (
            ('malatura', 'Malatura'),
            ('kalkomania', 'Kalkomania'),
        )),
        ('wyposażnie wewn.', 'Wyposażenie wewnętrzne'),
        ('wózek', 'Wózek'),
        ('urządz. ster. pojazdem', 'Urządzenia sterujące pojazdem'),
        ('urządz, monitoringu i bezpiecz.', 'Urządzenia monitoringu i bezpieczeństwa'),
        ('klima i orzewanie', 'Klimatyzacja i ogrzewanie'),
        ('drzwi', 'Drzwi'),
        ('sip', 'Urządzenia informacyjne'),
        ('układ hamowania', 'Układ hamowania'),
        ('układ sprzęgania', 'Układ sprzęgania'),
        ('okna i szyby', 'Okna i szyby'),
        ('układ elek.', 'Układ elektryczny'),
        ('Układ napędowy', (
            ('silnik', 'Silnik'),
            ('przekładnia', 'Przekładnia'),
        )),
        ('Wyposażenie zewnętrzne', (
            ('wycieraczki', 'Wycieraczki'),
            ('lusterka', 'Lusterka'),
            ('syreny', 'Syreny'),
        )),
        ('układ pneumatyczny', 'Układ pneumatyczny'),
    )
    name = models.CharField(max_length=40)
    category = models.CharField(max_length=50,
                                db_index=True,
                                choices=category_choices)
    description = models.TextField()
    actions = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    status = models.CharField(max_length=10,
                              choices=status_choices)
    entry_date = models.DateField()
    end_date = models.DateField(blank=True,
                                null=True)
    need = models.TextField(blank=True)
    vehicle = models.ForeignKey(Vehicle,
                                related_name='vehicle_faults_without_complaint',
                                on_delete=models.CASCADE)

    class Meta:
        ordering = ('entry_date',)

    def __str__(self):
        return self.name


class Part(models.Model):
    condition_choices = (
        ('new', 'New'),
        ('used', 'Used'),
        ('recovered', 'Recovered'),
    )
    origin_choices = (
        ('pesa', 'Pesa'),
        ('kw', 'Koleje Wielkopolskie'),
    )
    name = models.CharField(max_length=30,
                            db_index=True)
    index = models.CharField(max_length=50,
                             blank=True)
    condition = models.CharField(max_length=10,
                                 choices=condition_choices,
                                 db_index=True)
    assembly_date = models.DateField(blank=True,
                                     null=True)
    origin = models.CharField(max_length=20,
                              db_index=True,
                              choices=origin_choices)
    fault = models.ForeignKey(Fault,
                              related_name='parts',
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.name


