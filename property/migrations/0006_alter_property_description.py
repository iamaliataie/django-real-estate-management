# Generated by Django 4.2.3 on 2023-08-01 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0005_property_latitude_property_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='description',
            field=models.TextField(max_length=255),
        ),
    ]
