# Generated by Django 5.0.7 on 2024-07-24 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_remove_property_bathrooms_remove_property_bedrooms_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='land_size',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='property',
            name='price',
            field=models.CharField(max_length=255),
        ),
    ]
