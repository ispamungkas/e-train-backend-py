# Generated by Django 5.1.1 on 2025-03-08 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_training', '0005_rename_post_id_answer_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='ans',
            field=models.JSONField(default=dict, null=True),
        ),
    ]
