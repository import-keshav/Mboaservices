from django.db import models
from django.core.validators import MinValueValidator

from Restaurant import models as restaurant_models

class Dish(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    restaurant = models.ForeignKey(restaurant_models.Restaurant, on_delete=models.CASCADE, related_name="dishes_dish_restaurant", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=False, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'


class DishImage(models.Model):
    image = models.FileField(null=True, blank=True)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dishes_dish_image_dish", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'DishImage'
        verbose_name_plural = 'DishImages'
