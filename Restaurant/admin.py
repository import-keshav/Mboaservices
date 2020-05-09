from django.contrib import admin

from .models import (
	Restaurant,
	RestaurantEmployee,
	RestaurantImage,
	RestaurantPromocode,
	RestaurantDriver
)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
	list_display = ('name', 'owner', 'location_coordinates', 'is_open', 'address', 'id')
	search_fields = ('name', 'location_coordinates', 'address',
		'owner__name', 'owner__email', 'owner__mobile', 'id',
		'restaurant__id')


@admin.register(RestaurantEmployee)
class RestaurantEmployeeAdmin(admin.ModelAdmin):
	list_display = ('user', 'restaurant', 'id')
	search_fields = ('user__name', 'user__email', 'user__mobile',
		'restaurant__name', 'id', 'restaurant__id')


@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
	list_display = ('restaurant', 'image', 'id')
	search_fields = ('id', 'restaurant__id', 'restaurant__name')


@admin.register(RestaurantPromocode)
class RestaurantPromocodeAdmin(admin.ModelAdmin):
	list_display = ('promocode', 'restaurant', 'discount_percentage', 'valid_date', 'id')
	search_fields = ('id', 'restaurant__id', 'restaurant__name', 'promocode', 'valid_date')


@admin.register(RestaurantDriver)
class RestaurantDriverAdmin(admin.ModelAdmin):
	list_display = ('name', 'mobile', 'restaurant','image', 'id')
	search_fields = ('name', 'mobile', 'restaurant__name', 'restaurant__id', 'id')
