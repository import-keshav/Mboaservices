from django.contrib import admin

from .models import (
	Restaurant,
	RestaurantEmployee,
	RestaurantImage,
	RestaurantPromocode,
	RestaurantDriver
)

admin.site.register(Restaurant)
admin.site.register(RestaurantEmployee)
admin.site.register(RestaurantImage)
admin.site.register(RestaurantPromocode)
admin.site.register(RestaurantDriver)
