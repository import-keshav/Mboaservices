from django.contrib import admin


from .models import (
	Driver,
	DriverRestaurant
)


class DriverRestaurantInline(admin.TabularInline):
	model = DriverRestaurant
	extra = 1

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
	list_display = ('name', 'mobile', 'image', 'id')
	search_fields = ('name', 'mobile', 'id')
	inlines = (DriverRestaurantInline,)
