# Generated by Django 2.2 on 2020-07-11 00:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0010_auto_20200518_0549'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='rating',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]