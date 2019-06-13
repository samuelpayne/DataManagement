# Generated by Django 2.1.5 on 2019-06-07 19:42

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0074_auto_20190605_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentaldesign',
            name='_extra_fields_samples',
            field=django_mysql.models.ListTextField(models.CharField(blank=True, max_length=100, null=True), blank=True, null=True, size=None, verbose_name='Extra Fields for Samples'),
        ),
        migrations.AddField(
            model_name='sample',
            name='_extra_fields',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='_individual',
            field=models.ManyToManyField(blank=True, null=True, to='Records.Individual', verbose_name='Individual Identifier'),
        ),
        migrations.AlterField(
            model_name='experimentaldesign',
            name='_extra_fields',
            field=django_mysql.models.ListTextField(models.CharField(blank=True, max_length=100, null=True), blank=True, null=True, size=None, verbose_name='Extra Fields for Individuals'),
        ),
        migrations.AlterField(
            model_name='individual',
            name='_age',
            field=models.TextField(null=True, verbose_name='Age'),
        ),
        migrations.AlterField(
            model_name='individual',
            name='_gender',
            field=models.TextField(null=True, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='individual',
            name='_healthStatus',
            field=models.TextField(null=True, verbose_name='Health Status'),
        ),
    ]
