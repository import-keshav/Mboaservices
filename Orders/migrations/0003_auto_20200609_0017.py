# Generated by Django 2.2 on 2020-06-09 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0002_auto_20200606_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='client_address_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='client_coordinates',
            field=models.TextField(blank=True, null=True),
        ),
    ]
