# Generated by Django 5.1.1 on 2025-03-07 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0002_rename_date_training_dateline_section_is_deleted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='training',
            name='total_jp',
        ),
        migrations.AlterField(
            model_name='section',
            name='jp',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='section',
            name='status',
            field=models.CharField(choices=[('uncompleted', 'Uncompleted'), ('completed', 'Completed')], default='uncompleted', max_length=15),
        ),
        migrations.AlterField(
            model_name='section',
            name='train_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='trainings.training'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='section_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='trainings.section'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='status',
            field=models.CharField(choices=[('uncompleted', 'Uncompleted'), ('completed', 'Completed')], default='uncompleted', max_length=15),
        ),
        migrations.AlterField(
            model_name='training',
            name='type_train',
            field=models.CharField(choices=[('webinar', 'Webinar'), ('training', 'Training')], default='training', max_length=10),
        ),
        migrations.AlterField(
            model_name='training',
            name='type_train_ac',
            field=models.CharField(choices=[('online', 'Online'), ('offline', 'Offline')], default='online', max_length=10),
        ),
    ]
