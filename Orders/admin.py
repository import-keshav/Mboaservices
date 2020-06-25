from django.contrib import admin

from .models import (
	Order,
	OrderDish,
	IncomingOrder,
	OngoingOrder
)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Order._meta.fields]
	search_fields = ('restaurant__name', 'restaurant__location_coordinates'
		'client__user__name', 'client__user__email', 'client__user__mobile',
		'created', 'status', 'restaurant__id', 'client__id', 'delivered_time', 'id')


@admin.register(OrderDish)
class OrderDishAdmin(admin.ModelAdmin):
	list_display = ('order', 'dish', 'quantity', 'id')
	search_fields = ('order__restaurant__name',
		'order__restaurant__location_coordinates', 'dish__name',
		'order__id', 'order__restaurant__id', 'dish__id', 'id')


@admin.register(IncomingOrder)
class IncomingOrderAdmin(admin.ModelAdmin):
	list_display = [field.name for field in IncomingOrder._meta.fields]


@admin.register(OngoingOrder)
class OngoingOrderAdmin(admin.ModelAdmin):
	list_display = [field.name for field in OngoingOrder._meta.fields]