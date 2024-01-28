# Generated by Django 5.0.1 on 2024-01-28 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gingko', '0002_rename_completed_submission_completed_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='completed_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
