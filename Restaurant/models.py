from django.db import models
from django.core.validators import MinValueValidator

from User import models as user_models


class Restaurant(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    location_coordinates = models.CharField(max_length=30)
    client = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="restaurant_restaurant_client", null=True, blank=True)
    is_open = models.BooleanField(default=False, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'


class RestaurantEmployee(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_restaurant_employee_restaurant", null=True, blank=True)
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="user", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'RestaurantEmployee'
        verbose_name_plural = 'RestaurantEmployees'


class RestaurantImage(models.Model):
    image = models.FileField(null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_restaurant_image_restaurant", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'RestaurantImage'
        verbose_name_plural = 'RestaurantImages'


class RestaurantPromocode(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_restaurant_promocode_restaurant", null=True, blank=True)
    promocode = models.CharField(max_length=10, null=True, blank=True)
    discount_percentage = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'RestaurantPromocode'
        verbose_name_plural = 'RestaurantPromocodes'


class RestaurantDriver(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'RestaurantDriver'
        verbose_name_plural = 'RestaurantDrivers'
