# Generated by Django 2.1.5 on 2019-01-23 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0014_auto_20190123_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='dateCreated',
            field=models.DateTimeField(verbose_name='Date Created'),
        ),
    ]
