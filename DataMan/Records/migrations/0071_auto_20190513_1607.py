# Generated by Django 2.1.5 on 2019-05-13 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0070_auto_20190506_1203'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BackupFile',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='_treatmentProtocol',
        ),
        migrations.AddField(
            model_name='sample',
            name='_treatmentProtocol',
            field=models.ManyToManyField(blank=True, null=True, to='Records.Protocol', verbose_name='Treatment Protocol'),
        ),
    ]
