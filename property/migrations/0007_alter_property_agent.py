# Generated by Django 4.2.3 on 2023-08-27 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0006_property_type_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_properties', to=settings.AUTH_USER_MODEL),
        ),
    ]
