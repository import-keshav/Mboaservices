from django.db import models
from django.core.validators import MinValueValidator

from Restaurant import models as restaurant_models
from Client import models as client_models


class RestaurantRating(models.Model):
    restaurant = models.ForeignKey(restaurant_models.Restaurant, on_delete=models.CASCADE, related_name="restaurant_rating", null=True, blank=True)
    rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'RestaurantRating'
        verbose_name_plural = 'RestaurantRating'


class ClientReview(models.Model):
    client = models.ForeignKey(client_models.Client, on_delete=models.CASCADE, related_name="reviews_client_review_client", null=True, blank=True)
    restaurant = models.ForeignKey(restaurant_models.Restaurant, on_delete=models.CASCADE, related_name="reviews_client_review_restaurant", null=True, blank=True)
    points = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    comment = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'ClientReview'
        verbose_name_plural = 'ClientReviews'


class RestaurantReviewsInfo(models.Model):
    number_of_reviews = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    points = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'RestaurantReviewInfo'
        verbose_name_plural = 'RestaurantReviewsInfo'
