# Generated by Django 2.1.4 on 2018-12-31 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_auto_20181231_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='client',
            field=models.CharField(choices=[('KW', 'Koleje Wielkopolskie'), ('KL', 'Koleje Lubuskie')], max_length=50),
        ),
    ]
