# Generated by Django 2.1.5 on 2019-01-24 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0016_auto_20190123_1700'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataset',
            old_name='datasetID',
            new_name='_datasetID',
        ),
        migrations.RenameField(
            model_name='dataset',
            old_name='datasetName',
            new_name='_datasetName',
        ),
        migrations.RenameField(
            model_name='dataset',
            old_name='sample',
            new_name='_sample',
        ),
    ]
