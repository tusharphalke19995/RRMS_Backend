# Generated by Django 5.1.7 on 2025-04-08 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('caseInfoFiles', '0002_filedetails_classification_filedetails_filetype_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caseinfodetails',
            name='subject',
        ),
    ]
