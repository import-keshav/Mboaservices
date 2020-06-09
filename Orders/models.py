from django.db import models
from django.core.validators import MinValueValidator

from Client import models as client_models
from Restaurant import models as restaurant_models
from Dishes import models as dishes_models

payment_choices = (
	("Cash On Delivery", "Cash On Delivery"),
)

order_status = (
	("preparing", "preparing"),
	("packaging", "packaging"),
	("on_way", "on_way"),
    ("delivered", "delivered")
)


class Order(models.Model):
    restaurant = models.ForeignKey(restaurant_models.Restaurant, on_delete=models.CASCADE, related_name="orders_order_restaurant", null=True, blank=True)
    client = models.ForeignKey(client_models.Client, on_delete=models.CASCADE, related_name="orders_order_client", null=True, blank=True)
    payment_method = models.TextField(choices=payment_choices, null=True, blank=True)
    is_delivered = models.BooleanField(default=False, null=True, blank=True)
    is_accepted = models.BooleanField(default=False, null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    # transaction_id
    status = models.TextField(choices=order_status, null=True, blank=True)
    promocode_used = models.ForeignKey(restaurant_models.RestaurantPromocode, on_delete=models.CASCADE, related_name="orders_order_promocode_used", null=True, blank=True)
    client_coordinates = models.TextField(null=True, blank=True)
    client_address_details = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'
    def __str__(self):
        return self.restaurant.name


class OrderDish(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orders_order_dish_order", null=True, blank=True)
    dish = models.ForeignKey(dishes_models.Dish, on_delete=models.CASCADE, related_name="orders_order_dish_dish", null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Order Dish'
        verbose_name_plural = 'Order Dishes'
    def __str__(self):
        return self.dish.name