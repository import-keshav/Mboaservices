from django.contrib import admin

from .models import (
	Client, ClientCart, ClientNotification
)

admin.site.register(Client)
admin.site.register(ClientCart)
admin.site.register(ClientNotification)
