from django.db import models

from Restaurant import models as restaurant_models


class Driver(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    image = models.FileField(null=True, blank=True, upload_to="")

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'
    def __str__(self):
        return self.name


class DriverRestaurant(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="driver_driver_restaurant_driver", null=True, blank=True)
    restaurant = models.ForeignKey(restaurant_models.Restaurant, on_delete=models.CASCADE, related_name="driver_driver_restaurant_restaurant", null=True, blank=True)

    class Meta:
        verbose_name = 'Driver Restaurant'
        verbose_name_plural = 'Driver Restaurants'
