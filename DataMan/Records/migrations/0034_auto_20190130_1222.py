# Generated by Django 2.1.5 on 2019-01-30 19:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0033_dataset__experiment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='_acquisitionEnd',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Acquisition End'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='_acquisitionStart',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Acquisition Start'),
        ),
    ]
