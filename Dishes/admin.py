from django.contrib import admin

from .models import (
	Dish
)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
	list_display = ('name', 'restaurant', 'price', 'is_available', 'description' , 'image', 'get_category', 'id')
	search_fields = ('name', 'restaurant__name', 'price', 'restaurant__id', 'id')
	def get_category(self, obj):
		return [cat.name for cat in obj.categories.all()]
	get_category.short_description = 'Categories'
