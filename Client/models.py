from django.db import models
from django.core.validators import MinValueValidator

from User import models as user_models
from Dishes import models as dish_models
from Restaurant import models as restaurant_models


class Client(models.Model):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="client_client_user", null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    latitude = models.CharField(max_length=30, null=True, blank=True)
    longitude = models.CharField(max_length=30, null=True, blank=True)
    # category = models.CharField(max_length=50, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
    def __str__(self):
        return self.user.name


class ClientCart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_client_cart_client", null=True, blank=True)
    restaurant = models.ForeignKey(restaurant_models.Restaurant, on_delete=models.CASCADE, related_name="client_client_cart_client", null=True, blank=True)
    dish = models.ForeignKey(dish_models.Dish, on_delete=models.CASCADE, related_name="client_client_cart_client", null=True, blank=True)
    num_of_items = models.IntegerField(null=True, blank=True)
    add_ons = models.ManyToManyField(dish_models.DishAddOns, related_name="client_client_cart_dish_add_ons", null=True, blank=True)
    price = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Client Cart'
        verbose_name_plural = 'Client Carts'


class ClientNotification(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_client_notification_client", null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    notification_text = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Client Notification'
        verbose_name_plural = 'Client Notifications'
