from django.db import models
from django.urls import reverse


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


