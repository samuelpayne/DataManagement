# Generated by Django 2.1.5 on 2019-01-24 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0018_auto_20190123_1734'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataset',
            old_name='acquisitionEnd',
            new_name='_acquisitionEnd',
        ),
        migrations.RenameField(
            model_name='dataset',
            old_name='acquisitionStart',
            new_name='_acquisitionStart',
        ),
        migrations.RenameField(
            model_name='dataset',
            old_name='fileHash',
            new_name='_fileHash',
        ),
        migrations.RenameField(
            model_name='dataset',
            old_name='fileName',
            new_name='_fileName',
        ),
        migrations.RenameField(
            model_name='dataset',
            old_name='fileSize',
            new_name='_fileSize',
        ),
    ]
