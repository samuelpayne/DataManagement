# Generated by Django 2.1.5 on 2019-02-19 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0059_auto_20190213_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('_individualName', models.TextField(unique=True, verbose_name='Individual Name')),
                ('_individualID', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Individual ID')),
                ('_comments', models.TextField(blank=True, null=True, verbose_name='Comments, Notes, or Details')),
                ('_experiment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Records.Experiment', verbose_name='Experiment')),
            ],
            options={
                'ordering': ['_individualName'],
            },
        ),
        migrations.AlterField(
            model_name='fileread',
            name='lead',
            field=models.CharField(max_length=200, verbose_name='Project Lead'),
        ),
    ]
