# Generated by Django 5.1.7 on 2025-03-16 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_is_staff_remove_user_roles_user_roles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='roles',
            new_name='role',
        ),
    ]
