# Generated by Django 2.1.5 on 2019-01-16 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datasetName', models.TextField(help_text='Dataset Name')),
                ('datasetID', models.IntegerField(help_text='Dataset ID')),
                ('instrumentSetting', models.TextField(help_text='link to instrument settings')),
                ('type', models.TextField(help_text='Type of data generated')),
                ('operator', models.TextField(help_text='Operator')),
                ('status', models.TextField(help_text='Status')),
                ('dateCreated', models.DateTimeField()),
                ('fileLocation', models.TextField(help_text='Path to file location')),
                ('fileName', models.TextField(help_text='File Name')),
                ('acquisitionStart', models.TextField(help_text='Acquisition Start')),
                ('acquisitionEnd', models.TextField(help_text='Acquisition End')),
                ('fileSize', models.IntegerField(help_text='File Size')),
                ('fileHash', models.TextField(help_text='File Hash')),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experimentName', models.TextField(help_text='Experiment Name')),
                ('experimentID', models.IntegerField(help_text='Experiment ID')),
                ('projectLead', models.TextField(help_text='Project Lead')),
                ('teamMembers', models.TextField(help_text='Team Members')),
                ('IRB', models.IntegerField(help_text='IRB Number')),
                ('experimentalDesign', models.TextField(help_text='Experimental Design')),
                ('datasets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sampleName', models.TextField(help_text='Sample Name')),
                ('sampleID', models.IntegerField(help_text='Integer Field')),
                ('storageCondition', models.TextField(help_text='Storage Condition')),
                ('storageLocation', models.TextField(help_text='Path to storage location')),
                ('treatmentProtocol', models.TextField(help_text='Treatment Protocol')),
                ('dateCreated', models.DateTimeField()),
                ('organism', models.TextField(help_text='Organism')),
                ('organismModifications', models.TextField(help_text='Organism Modifications')),
                ('datasets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.Dataset')),
            ],
        ),
        migrations.AddField(
            model_name='experiment',
            name='samples',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.Sample'),
        ),
    ]
