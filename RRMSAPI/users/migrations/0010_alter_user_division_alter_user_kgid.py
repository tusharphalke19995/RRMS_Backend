# Generated by Django 5.1.7 on 2025-03-18 18:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_rename_divisionid_user_division'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='division',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.divisionmaster'),
        ),
        migrations.AlterField(
            model_name='user',
            name='kgid',
            field=models.CharField(default=None, max_length=20, null=True, unique=True),
        ),
    ]
