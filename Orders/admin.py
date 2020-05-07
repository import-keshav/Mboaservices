from django.contrib import admin

from .models import (
	Order,
	OrderDish
)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = (
		'restaurant', 'client', 'date', 'time', 'payment_method',
		'is_delivered', 'is_accepted', 'total_amount', 'status')


@admin.register(OrderDish)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('order', 'dish', 'quantity')
