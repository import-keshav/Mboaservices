from django.contrib import admin

from .models import (
	Dish,
	DishImage
)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
	list_display = ('name', 'restaurant', 'price', 'is_available', 'description' , 'id')
	search_fields = ('name', 'restaurant__name', 'price', 'restaurant__id', 'id')


@admin.register(DishImage)
class DishImageAdmin(admin.ModelAdmin):
	list_display = ('dish', 'image', 'id')
	search_fields = ('dish__name', 'dish__restaurant__name',
		'dish__id', 'dish__restaurant__id', 'id')
