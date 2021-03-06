# Generated by Django 2.1.5 on 2019-01-24 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0025_auto_20190123_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='_experiment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Records.Experiment', verbose_name='Experiment'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='_sampleID',
            field=models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Sample ID'),
        ),
    ]
