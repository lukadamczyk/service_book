# Generated by Django 2.1.4 on 2019-01-01 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0012_auto_20190101_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fault',
            name='actions',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='fault',
            name='comments',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='fault',
            name='zr_number',
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
    ]
