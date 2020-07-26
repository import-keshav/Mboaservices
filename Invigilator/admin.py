from django.contrib import admin

from .models import (
	Invigilator,
	InvigilatorOrderAssignment,
	InvigilatorClientMessage
)


@admin.register(Invigilator)
class InvigilatorAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Invigilator._meta.fields]
	search_fields = ('user__name', 'user__email', 'user__mobile',
		'city', 'latitude', 'longitude', 'id')


@admin.register(InvigilatorOrderAssignment)
class InvigilatorOrderAssignmentAdmin(admin.ModelAdmin):
	list_display = [field.name for field in InvigilatorOrderAssignment._meta.fields]
	search_fields = ('invigilator__user__nam','invigilator__user__email',
		'invigilator__user__mobile', 'order__id', 'order__restaurant'
		'id')

@admin.register(InvigilatorClientMessage)
class InvigilatorClientMessageAdmin(admin.ModelAdmin):
	list_display = [field.name for field in InvigilatorClientMessage._meta.fields]
