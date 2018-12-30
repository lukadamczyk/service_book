from django.db import models
from django.urls import reverse


class Vehicle(models.Model):
    number = models.CharField(max_length=10)
    vehicle_type = models.CharField(max_length=10,
                                    db_index=True,)
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


# Create your models here.
