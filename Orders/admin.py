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
	search_fields = ('restaurant__name', 'restaurant__latitude', 'restaurant__longitude',
		'client__user__name', 'client__user__email', 'client__user__mobile',
		'created', 'status', 'restaurant__id', 'client__id', 'delivered_time', 'id')
	inlines = [OrderDishTabularInline,]


@admin.register(IncomingOrder)
class IncomingOrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'order', 'get_order_id', 'restaurant', 'get_restaurant_id']
	def get_order_id(self, obj):
		return obj.order.id
	get_order_id.short_description = 'Order ID'

	def get_restaurant_id(self, obj):
		return obj.restaurant.id
	get_restaurant_id.short_description = 'Restaurant ID'



@admin.register(OngoingOrder)
class OngoingOrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'order', 'get_order_id', 'restaurant', 'get_restaurant_id']
	def get_order_id(self, obj):
		return obj.order.id
	get_order_id.short_description = 'Order ID'

	def get_restaurant_id(self, obj):
		return obj.restaurant.id
	get_restaurant_id.short_description = 'Restaurant ID'
