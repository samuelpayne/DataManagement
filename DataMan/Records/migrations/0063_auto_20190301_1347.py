# Generated by Django 2.1.5 on 2019-03-01 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0062_experimentaldesign__extra_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='_sample',
            field=models.ManyToManyField(to='Records.Sample', verbose_name='Sample'),
        ),
        migrations.AlterField(
            model_name='individual',
            name='_individualIdentifier',
            field=models.TextField(unique=True, verbose_name='Individual Identifier'),
        ),
    ]
