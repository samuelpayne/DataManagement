# Generated by Django 2.1.5 on 2019-01-24 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0015_auto_20190123_1654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataset',
            old_name='instrumentSetting',
            new_name='_instrumentSetting',
        ),
    ]
