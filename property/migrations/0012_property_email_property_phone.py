# Generated by Django 4.2.3 on 2023-08-13 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0011_property_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='email',
            field=models.EmailField(default='netlinks.realestate@gmail.com', max_length=100),
        ),
        migrations.AddField(
            model_name='property',
            name='phone',
            field=models.CharField(default='+93783767956', max_length=20),
        ),
    ]
