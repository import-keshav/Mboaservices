# Generated by Django 2.2 on 2020-07-07 16:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client', '0002_clientcart_add_ons'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientcart',
            name='price',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]