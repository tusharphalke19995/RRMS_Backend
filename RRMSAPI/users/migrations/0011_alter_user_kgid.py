# Generated by Django 5.1.7 on 2025-03-18 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_user_division_alter_user_kgid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='kgid',
            field=models.CharField(default=None, max_length=20, unique=True),
        ),
    ]
