# Generated by Django 2.2 on 2020-07-26 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0007_orderdish_add_ons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='client_coordinates',
        ),
        migrations.AddField(
            model_name='order',
            name='latitude',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='longitude',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
