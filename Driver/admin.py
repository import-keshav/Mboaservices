from django.contrib import admin

# Register your models here.
from .models import Driver

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
	list_display = ('name', 'mobile', 'image', 'id')
	search_fields = ('name', 'mobile', 'id')
