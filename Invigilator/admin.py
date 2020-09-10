from django.contrib import admin

from .models import (
	Invigilator,
	InvigilatorRestaurant,
	InvigilatorClientMessage
)

class InvigilatorRestaurantInline(admin.TabularInline):
	model = InvigilatorRestaurant
	extra = 1

@admin.register(Invigilator)
class InvigilatorAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Invigilator._meta.fields]
	search_fields = ('user__name', 'user__email', 'user__mobile',
		'city', 'latitude', 'longitude', 'id')
	inlines = (InvigilatorRestaurantInline,)


@admin.register(InvigilatorClientMessage)
class InvigilatorClientMessageAdmin(admin.ModelAdmin):
	list_display = [field.name for field in InvigilatorClientMessage._meta.fields]
