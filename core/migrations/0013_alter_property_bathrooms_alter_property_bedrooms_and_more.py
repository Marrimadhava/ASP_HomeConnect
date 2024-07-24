# Generated by Django 5.0.7 on 2024-07-24 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_property_salesperson_property_bathrooms_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='bathrooms',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='bedrooms',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='land_size',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='property',
            name='price',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='property',
            name='square_footage',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='year_built',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
