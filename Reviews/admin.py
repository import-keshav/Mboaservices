from django.contrib import admin

from .models import (
	ClientReview,
	RestaurantReviewsInfo
)


@admin.register(ClientReview)
class ClientReviewAdmin(admin.ModelAdmin):
	list_display = ('client', 'restaurant', 'points', 'comment', 'id')
	search_fields = ('restaurant__name', 'restaurant__latitude', 'restaurant__longitude',
		'client__user__name', 'client__user__email', 'client__user__mobile', 
		'restaurant__id', 'client__id', 'comment', 'id')


@admin.register(RestaurantReviewsInfo)
class RestaurantReviewsInfoAdmin(admin.ModelAdmin):
	list_display = ('restaurant', 'number_of_reviews', 'points', 'id')
	search_fields = ('restaurant__name', 'restaurant__id', 'id')
