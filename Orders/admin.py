from django.contrib import admin

from .models import (
	Order,
	OrderDish,
	IncomingOrder,
	OngoingOrder
)

class OrderDishTabularInline(admin.TabularInline):
    model = OrderDish
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Order._meta.fields]
	search_fields = ('restaurant__name', 'restaurant__location_coordinates'
		'client__user__name', 'client__user__email', 'client__user__mobile',
		'created', 'status', 'restaurant__id', 'client__id', 'delivered_time', 'id')
	inlines = [OrderDishTabularInline,]


@admin.register(IncomingOrder)
class IncomingOrderAdmin(admin.ModelAdmin):
	list_display = [field.name for field in IncomingOrder._meta.fields]


@admin.register(OngoingOrder)
class OngoingOrderAdmin(admin.ModelAdmin):
	list_display = [field.name for field in OngoingOrder._meta.fields]