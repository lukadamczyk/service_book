# Generated by Django 2.1.4 on 2019-01-05 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0017_auto_20190101_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('KW', 'Koleje Wielkopolskie'), ('KD', 'Koleje Dolnośląskie'), ('KL', 'Koleje Lubuskie')], db_index=True, max_length=20)),
                ('city', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
            ],
        ),
    ]