from django.db import models
from django.urls import reverse
from django.conf import settings


class Vehicle(models.Model):
    choices = (
        ('SA132', 'SA132'),
        ('SA134', 'SA134'),
        ('SA139', 'SA139'),
    )
    number = models.CharField(max_length=10)
    vehicle_type = models.CharField(max_length=10,
                                    db_index=True,
                                    choices=choices)
    slug = models.SlugField(max_length=20,
                            db_index=True,
                            unique=True)
    trolleys = models.CharField(max_length=10,
                                unique=True)
    warranty = models.DateField()

    def __str__(self):
        return 'Pojazd: {}-{}'.format(self.vehicle_type, self.number)

    def get_absolute_url(self):
        return reverse('book:vehicle_detail',
                       args=[self.id, self.slug])


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
    date = models.DateField(null=True)
    inspection_type = models.CharField(max_length=10,
                                       db_index=True,
                                       null=True,
                                       choices=choices)
    performer = models.CharField(max_length=30,
                                 db_index=True,
                                 null=True)
    vehicle = models.ForeignKey(Vehicle,
                                related_name='vehicles',
                                on_delete=models.CASCADE,
                                null=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return 'Przegląd: {}, dzień wykonania: {}.{}.{}'.format(self.inspection_type, self.date.day, self.date.month,
                                                                self.date.year)


class Complaint(models.Model):
    status_choices = (
        ('open', 'Open'),
        ('close', 'Close')
    )
    client_choices = (
        ('KW', 'Koleje Wielkopolskie'),
        ('KL', 'Koleje Lubuskie')
    )
    document_number = models.CharField(max_length=50)
    entry_date = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(blank=True,
                                    null=True)
    status = models.CharField(max_length=10,
                              choices=status_choices)
    tasks = models.TextField(blank=True,
                             null=True)
    client = models.CharField(max_length=50,
                              choices=client_choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle,
                                related_name='complaint_vehicles',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.document_number

    class Meta:
        ordering = ('-entry_date',)


class Fault(models.Model):
    status_choices = (
        ('open', 'Open'),
        ('close', 'Close')
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
    name = models.CharField(max_length=20)
    category = models.CharField(max_length=50,
                                db_index=True,
                                choices=category_choices)
    description = models.TextField()
    actions = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    zr_number = models.CharField(max_length=10,
                                 unique=True,
                                 blank=True)
    status = models.CharField(max_length=10,
                              choices=status_choices)
    end_date = models.DateField(blank=True,
                                null=True)
    complaint = models.ForeignKey(Complaint,
                                  related_name='complaint_faults',
                                  on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle,
                                related_name='vehicle_faults',
                                on_delete=models.CASCADE)

