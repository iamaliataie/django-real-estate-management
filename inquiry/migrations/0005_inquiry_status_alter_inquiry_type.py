# Generated by Django 4.2.3 on 2023-08-07 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry', '0004_inquiry_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='status',
            field=models.CharField(blank=True, choices=[('read', 'Read'), ('unread', 'unread')], default='unread', max_length=6, null=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='type',
            field=models.CharField(choices=[('information', 'Information'), ('sales', 'About Sales'), ('payment', 'About Payment'), ('schedule', 'About Schedule')], max_length=30, verbose_name='Topic'),
        ),
    ]
