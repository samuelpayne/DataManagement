# Generated by Django 2.1.5 on 2019-01-23 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0013_auto_20190122_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='dateCreated',
            field=models.DateTimeField(verbose_name='Date Created'),
        ),
    ]
