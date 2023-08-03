# Generated by Django 4.2.3 on 2023-08-03 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_alter_property_price'),
        ('inquiry', '0002_inquiry_property'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquiry',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inquiries', to='property.property'),
        ),
    ]
