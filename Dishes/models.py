from django.db import models
from django.core.validators import MinValueValidator

from Restaurant import models as restaurant_models

class GeneralDish(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    categories = models.ManyToManyField(restaurant_models.RestraurantDishesCategory)
    image = models.FileField(null=True, blank=True, upload_to="")

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'General Dish'
        verbose_name_plural = 'General Dishes'
    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    restaurant = models.ForeignKey(restaurant_models.Restaurant, on_delete=models.CASCADE, related_name="dishes_dish_restaurant", null=True, blank=True)
    price = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    adds_on = models.TextField(null=True,blank=True)
    categories = models.ManyToManyField(restaurant_models.RestraurantDishesCategory)
    image = models.FileField(null=True, blank=True, upload_to="")

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Dish'
        verbose_name_plural = 'Dishes'
    def __str__(self):
        return self.name
    def save(self):
        if self.name:
            self.name = self.name.lower()
        super(Dish, self).save()



class DishAddOns(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dishes_dishaddons_dish", null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    is_free = models.BooleanField(default=False, null=True, blank=True)
    is_available = models.BooleanField(default=False, null=True, blank=True)
    price = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Dish Add On'
        verbose_name_plural = 'Dish Add Ons'
    def __str__(self):
        return self.name
