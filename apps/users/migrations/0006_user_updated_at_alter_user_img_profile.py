# Generated by Django 5.1.1 on 2025-03-05 14:04

import apps.users.models
import time
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.IntegerField(default=time.time),
        ),
        migrations.AlterField(
            model_name='user',
            name='img_profile',
            field=models.ImageField(null=True, upload_to=apps.users.models.file_location),
        ),
    ]
