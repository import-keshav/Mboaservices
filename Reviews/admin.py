from django.contrib import admin

from .models import (
	RestaurantRating,
	ClientReview,
	RestaurantReviewsInfo
)

admin.site.register(RestaurantRating)
admin.site.register(ClientReview)
admin.site.register(RestaurantReviewsInfo)