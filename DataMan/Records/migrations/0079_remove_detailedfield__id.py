# Generated by Django 2.1.5 on 2019-06-21 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0078_detailedfield__id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detailedfield',
            name='_id',
        ),
    ]
