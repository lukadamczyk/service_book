# Generated by Django 2.1.4 on 2018-12-31 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_vehicle_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspection',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='inspection',
            name='inspection_type',
            field=models.CharField(db_index=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='inspection',
            name='performer',
            field=models.CharField(db_index=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='inspection',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='book.Vehicle'),
        ),
    ]