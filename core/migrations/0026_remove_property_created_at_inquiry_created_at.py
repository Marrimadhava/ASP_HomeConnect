# Generated by Django 5.0.7 on 2024-07-29 00:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_property_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='created_at',
        ),
        migrations.AddField(
            model_name='inquiry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
