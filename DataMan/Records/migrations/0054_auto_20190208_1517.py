# Generated by Django 2.1.5 on 2019-02-08 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0053_auto_20190208_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileread',
            name='_File',
            field=models.FilePathField(),
        ),
    ]
