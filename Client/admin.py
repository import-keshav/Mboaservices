from django.contrib import admin

from .models import (
	Client, ClientCart, ClientNotification
)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	list_display = ('user', 'location_coordinates', 'address')


@admin.register(ClientCart)
class ClientCartAdmin(admin.ModelAdmin):
	list_display = ('client', 'restaurant', 'dish', 'num_of_items')


@admin.register(ClientNotification)
class ClientNotificationAdmin(admin.ModelAdmin):
	list_display = ('client', 'date', 'time', 'notification_text')
