# Generated by Django 2.1.5 on 2019-01-22 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0011_merge_20190122_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='acquisitionEnd',
            field=models.TextField(verbose_name='Acquisition End'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='acquisitionStart',
            field=models.TextField(verbose_name='Acquisition Start'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='datasetID',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Dataset ID'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='datasetName',
            field=models.TextField(unique=True, verbose_name='Dataset Name'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='fileHash',
            field=models.TextField(verbose_name='File Hash'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='fileLocation',
            field=models.TextField(verbose_name='Path to file location'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='fileName',
            field=models.TextField(verbose_name='File Name'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='fileSize',
            field=models.IntegerField(verbose_name='File Size'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='instrumentSetting',
            field=models.TextField(verbose_name='link to instrument settings'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='operator',
            field=models.TextField(verbose_name='Operator'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='status',
            field=models.TextField(verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='type',
            field=models.TextField(verbose_name='Type of data generated'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='IRB',
            field=models.IntegerField(verbose_name='IRB Number'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='experimentID',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Experiment ID'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='experimentName',
            field=models.TextField(unique=True, verbose_name='Experiment Name'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='experimentalDesign',
            field=models.TextField(verbose_name='Experimental Design'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='projectLead',
            field=models.TextField(verbose_name='Project Lead'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='teamMembers',
            field=models.TextField(verbose_name='Team Members'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='dateCreated',
            field=models.DateTimeField(help_text='Date the sample was taken'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='organism',
            field=models.TextField(verbose_name='Organism'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='organismModifications',
            field=models.TextField(default='None', verbose_name='Organism Modifications'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sampleID',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sampleName',
            field=models.TextField(unique=True, verbose_name='Sample Name'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='storageCondition',
            field=models.TextField(verbose_name='Storage Condition'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='storageLocation',
            field=models.TextField(verbose_name='Storage Location'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='treatmentProtocol',
            field=models.TextField(verbose_name='Treatment Protocol'),
        ),
    ]
