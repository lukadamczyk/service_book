# Generated by Django 2.1.4 on 2019-01-05 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0021_remove_choices_for_name_model_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
