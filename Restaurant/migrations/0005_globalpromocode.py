# Generated by Django 2.2 on 2020-09-15 11:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0004_restaurant_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalPromocode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promocode', models.CharField(blank=True, max_length=10, null=True)),
                ('discount_percentage', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('valid_date', models.DateField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Global Promocode',
                'verbose_name_plural': 'Global Promocodes',
            },
        ),
    ]
