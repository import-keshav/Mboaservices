from django.contrib import admin

from .models import (
	Order,
	OrderDish
)

admin.site.register(Order)
admin.site.register(OrderDish)
