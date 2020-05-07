# Generated by Django 3.0.5 on 2020-05-07 11:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Restaurant', '0001_initial'),
        ('Client', '0001_initial'),
        ('Dishes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('payment_method', models.TextField(blank=True, choices=[('Cash On Delivery', 'Cash On Delivery')], null=True)),
                ('is_delivered', models.BooleanField(blank=True, default=False, null=True)),
                ('is_accepted', models.BooleanField(blank=True, default=False, null=True)),
                ('total_amount', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.TextField(blank=True, choices=[('preparing', 'preparing'), ('packaging', 'packaging'), ('on_way', 'on_way'), ('delivered', 'delivered')], null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_order_client', to='Client.Client')),
                ('promocode_used', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_order_promocode_used', to='Restaurant.RestaurantPromocode')),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_order_restaurant', to='Restaurant.Restaurant')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Order',
            },
        ),
        migrations.CreateModel(
            name='OrderDish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('dish', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_order_dish_dish', to='Dishes.Dish')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_order_dish_order', to='Orders.Order')),
            ],
            options={
                'verbose_name': 'Order Dish',
                'verbose_name_plural': 'Order Dishes',
            },
        ),
    ]
