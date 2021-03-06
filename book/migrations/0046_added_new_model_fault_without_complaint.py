# Generated by Django 2.2.13 on 2020-07-17 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0045_addded_vehicle_choice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fault_without_complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('category', models.CharField(choices=[('pudło', (('nadwozie', 'Nadwozie'), ('poszycie', 'Poszycie'), ('podłoga', 'Podłoga'), ('konstrukcja', 'Konstrukcja'), ('układy nośne', 'Układy nośne'), ('grodzenia', 'Grodzenia'))), ('materiały wykończeniowe', (('malatura', 'Malatura'), ('kalkomania', 'Kalkomania'))), ('wyposażnie wewn.', 'Wyposażenie wewnętrzne'), ('wózek', 'Wózek'), ('urządz. ster. pojazdem', 'Urządzenia sterujące pojazdem'), ('urządz, monitoringu i bezpiecz.', 'Urządzenia monitoringu i bezpieczeństwa'), ('klima i orzewanie', 'Klimatyzacja i ogrzewanie'), ('drzwi', 'Drzwi'), ('sip', 'Urządzenia informacyjne'), ('układ hamowania', 'Układ hamowania'), ('układ sprzęgania', 'Układ sprzęgania'), ('okna i szyby', 'Okna i szyby'), ('układ elek.', 'Układ elektryczny'), ('Układ napędowy', (('silnik', 'Silnik'), ('przekładnia', 'Przekładnia'))), ('Wyposażenie zewnętrzne', (('wycieraczki', 'Wycieraczki'), ('lusterka', 'Lusterka'), ('syreny', 'Syreny'))), ('układ pneumatyczny', 'Układ pneumatyczny')], db_index=True, max_length=50)),
                ('description', models.TextField()),
                ('actions', models.TextField(blank=True)),
                ('comments', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('open', 'Otwarta'), ('close', 'Zamknięta')], max_length=10)),
                ('entry_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('need', models.TextField(blank=True)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_faults_without_complaint', to='book.Vehicle')),
            ],
            options={
                'ordering': ('entry_date',),
            },
        ),
    ]
