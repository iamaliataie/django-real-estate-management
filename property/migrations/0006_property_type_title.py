# Generated by Django 4.2.3 on 2023-08-22 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0005_property_marker_color_property_type_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='type_title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
