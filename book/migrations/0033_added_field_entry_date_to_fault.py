# Generated by Django 2.1.4 on 2019-01-08 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0032_alter_datetime_to_date_in_complaint'),
    ]

    operations = [
        migrations.AddField(
            model_name='fault',
            name='entry_date',
            field=models.DateField(default='2019-1-1'),
            preserve_default=False,
        ),
    ]
