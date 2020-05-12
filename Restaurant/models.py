from django.db import models
from django.core.validators import MinValueValidator

from User import models as user_models


class Restaurant(models.Model):
    unique_id = models.CharField(max_length=10, null=True, blank=True, unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    owner = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="restaurant_restaurant_client", null=True, blank=True)
    location_coordinates = models.CharField(max_length=30)
    is_open = models.BooleanField(default=False, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'
    def __str__(self):
        return self.name


class RestaurantEmployee(models.Model):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="user", null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_restaurant_employee_restaurant", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Restaurant Employee'
        verbose_name_plural = 'Restaurant Employees'
    def __str__(self):
        return self.user.name


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_restaurant_image_restaurant", null=True, blank=True)
    image = models.FileField(null=True, blank=True, upload_to="")

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Restaurant Image'
        verbose_name_plural = 'Restaurant Images'
    def __str__(self):
        return self.restaurant.name


class RestaurantPromocode(models.Model):
    promocode = models.CharField(max_length=10, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_restaurant_promocode_restaurant", null=True, blank=True)
    discount_percentage = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    valid_date = models.DateField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Restaurant Promocode'
        verbose_name_plural = 'Restaurant Promocodes'
    def __str__(self):
        return self.promocode


class RestaurantDriver(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_restaurant_driver_restaurant", null=True, blank=True)
    image = models.FileField(null=True, blank=True, upload_to="")

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Restaurant Driver'
        verbose_name_plural = 'Restaurant Drivers'
    def __str__(self):
        return self.name