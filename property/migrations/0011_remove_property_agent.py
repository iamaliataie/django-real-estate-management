# Generated by Django 4.2.3 on 2023-08-07 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0010_property_agent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='agent',
        ),
    ]
