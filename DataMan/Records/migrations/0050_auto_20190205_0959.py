# Generated by Django 2.1.5 on 2019-02-05 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0049_auto_20190204_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='_instrumentSetting',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Records.InstrumentSetting', verbose_name='Instrument Setting'),
        ),
    ]
