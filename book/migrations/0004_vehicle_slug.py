# Generated by Django 2.1.4 on 2018-12-30 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_auto_20181230_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='slug',
            field=models.SlugField(default='adsfa', max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
