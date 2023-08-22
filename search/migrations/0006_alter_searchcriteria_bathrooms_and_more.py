# Generated by Django 4.2.3 on 2023-08-22 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_searchcriteria_basement_searchcriteria_bathrooms_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchcriteria',
            name='bathrooms',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='bedrooms',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='floors',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='parking',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='price_from',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='price_to',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
