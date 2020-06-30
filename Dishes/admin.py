from django.contrib import admin

from .models import (
	Dish,
	DishAddOns
)

class DishAddOnsTabularInline(admin.TabularInline):
	model = DishAddOns
	extra = 1

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
	list_display = ('name', 'restaurant', 'price', 'is_available', 'description' , 'image', 'get_category', 'id')
	search_fields = ('name', 'restaurant__name', 'price', 'restaurant__id', 'id')
	list_filter = ('name', 'restaurant', 'categories')
	inlines = (DishAddOnsTabularInline,)
	def get_category(self, obj):
		return [cat.name for cat in obj.categories.all()]
	get_category.short_description = 'Categories'


@admin.register(DishAddOns)
class DishAddOnsAdmin(admin.ModelAdmin):
	list_display = ('name', 'dish', 'is_free', 'price', 'id')
	search_fields = ('name', 'dish__name')
	raw_id_fields = ('dish',)
	list_filter = ('name', 'dish', 'is_free')
