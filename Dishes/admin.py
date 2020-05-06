from django.contrib import admin

from .models import (
	Dish,
	DishImage
)

admin.site.register(Dish)
admin.site.register(DishImage)
