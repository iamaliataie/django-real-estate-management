# Generated by Django 4.2.3 on 2023-08-20 05:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0017_property_features'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='location',
            new_name='address',
        ),
        migrations.AddField(
            model_name='property',
            name='city',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
