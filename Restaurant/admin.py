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
	list_display = ('name', 'owner', 'location_coordinates', 'is_open', 'address')


@admin.register(RestaurantEmployee)
class RestaurantEmployeeAdmin(admin.ModelAdmin):
	list_display = ('user', 'restaurant')



@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
	list_display = ('restaurant', 'image')


@admin.register(RestaurantPromocode)
class RestaurantPromocodeAdmin(admin.ModelAdmin):
	list_display = ('promocode', 'restaurant', 'discount_percentage')


@admin.register(RestaurantDriver)
class RestaurantDriverAdmin(admin.ModelAdmin):
	list_display = ('name', 'mobile')

