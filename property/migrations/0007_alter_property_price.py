# Generated by Django 4.2.3 on 2023-08-01 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_alter_property_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]
