from django.contrib import admin

from .models import (
	Order,
	OrderDish
)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = (
		'restaurant', 'client', 'date', 'time', 'payment_method',
		'is_delivered', 'is_accepted', 'total_amount', 'status', 'id')
	search_fields = ('restaurant__name', 'restaurant__location_coordinates'
		'client__user__name', 'client__user__email', 'client__user__mobile',
		'date', 'time', 'status', 'restaurant__id', 'client__id', 'id')


@admin.register(OrderDish)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('order', 'dish', 'quantity', 'id')
	search_fields = ('order__restaurant__name',
		'order__restaurant__location_coordinates', 'dish__name',
		'order__id', 'order__restaurant__id', 'dish__id', 'id')
