from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from Restaurant import models as restaurant_models
from Client import models as client_models


class RestaurantRating(models.Model):
    restaurant = models.ForeignKey(restaurant_models.Restaurant, on_delete=models.CASCADE, related_name="restaurant_rating", null=True, blank=True)
    rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Restaurant Rating'
        verbose_name_plural = 'Restaurant Rating'
    def __str__(self):
        return self.restaurant.name


class ClientReview(models.Model):
    client = models.ForeignKey(client_models.Client, on_delete=models.CASCADE, related_name="reviews_client_review_client", null=True, blank=True)
    restaurant = models.ForeignKey(restaurant_models.Restaurant, on_delete=models.CASCADE, related_name="reviews_client_review_restaurant", null=True, blank=True)
    points = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Client Review'
        verbose_name_plural = 'Client Reviews'
    def __str__(self):
        return self.client.user.name


class RestaurantReviewsInfo(models.Model):
    restaurant = models.ForeignKey(restaurant_models.Restaurant, on_delete=models.CASCADE, related_name="reviews_restaurant_review_restaurant", null=True, blank=True)
    number_of_reviews = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    points = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Restaurant ReviewInfo'
        verbose_name_plural = 'Restaurant Reviews Info'
