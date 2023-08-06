# Generated by Django 4.2.3 on 2023-08-06 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0008_alter_property_price'),
        ('account', '0004_user_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='users', to='property.property'),
        ),
    ]
