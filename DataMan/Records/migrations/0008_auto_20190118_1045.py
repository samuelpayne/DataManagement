# Generated by Django 2.1.5 on 2019-01-18 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0007_dataset_sample'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='id',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='datasets',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='id',
        ),
        migrations.AlterField(
            model_name='dataset',
            name='datasetID',
            field=models.IntegerField(help_text='Dataset ID', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='experimentID',
            field=models.IntegerField(help_text='Experiment ID', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sampleName',
            field=models.TextField(verbose_name='Sample Name'),
        ),
    ]
