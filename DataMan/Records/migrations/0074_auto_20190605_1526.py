# Generated by Django 2.1.5 on 2019-06-05 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0073_auto_20190605_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailedfield',
            name='_files',
            field=models.ManyToManyField(blank=True, to='Records.File', verbose_name='Files'),
        ),
        migrations.AlterField(
            model_name='file',
            name='_file',
            field=models.FileField(upload_to='C:\\Users\\M McCown\\SCS\\DataMan\\media/files/%Y/%m/%d/', verbose_name='File'),
        ),
    ]
