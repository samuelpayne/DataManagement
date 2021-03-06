# Generated by Django 2.1.5 on 2019-02-08 21:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0052_auto_20190207_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='_acquisitionEnd',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Acquisition End'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='_acquisitionStart',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Acquisition Start'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='_fileName',
            field=models.TextField(null=True, verbose_name='File Name'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='_operator',
            field=models.TextField(blank=True, help_text='The team member who ran the machine.', null=True, verbose_name='Operator'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='_sample',
            field=models.ManyToManyField(null=True, to='Records.Sample', verbose_name='Sample'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='_type',
            field=models.TextField(blank=True, null=True, verbose_name='Type of data generated'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='_experimentalDesign',
            field=models.TextField(null=True, verbose_name='Experimental Design'),
        ),
        migrations.AlterField(
            model_name='fileread',
            name='_File',
            field=models.FileField(upload_to='files/'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='_experiment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Records.Experiment', verbose_name='Experiment'),
        ),
    ]
