from django.contrib import admin

from .models import (
	RestaurantRating,
	ClientReview,
	RestaurantReviewsInfo
)

@admin.register(RestaurantRating)
class RestaurantRatingAdmin(admin.ModelAdmin):
	list_display = ('restaurant', 'rating')


@admin.register(ClientReview)
class ClientReviewAdmin(admin.ModelAdmin):
	list_display = ('client', 'restaurant', 'points', 'comment')

@admin.register(RestaurantReviewsInfo)
class RestaurantReviewsInfoAdmin(admin.ModelAdmin):
	list_display = ('restaurant', 'number_of_reviews', 'points')