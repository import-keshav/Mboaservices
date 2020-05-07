from django.contrib import admin

from .models import (
	Dish,
	DishImage
)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
	list_display = ('name', 'restaurant', 'price', 'is_available', 'description')


@admin.register(DishImage)
class DishImageAdmin(admin.ModelAdmin):
	list_display = ('dish', 'image')
