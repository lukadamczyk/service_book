# Generated by Django 2.1.4 on 2018-12-31 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_auto_20181231_1859'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inspection',
            options={'ordering': ('-date',)},
        ),
    ]
