from django.db import models
from django.core.validators import MinValueValidator

from Client import models as client_models
from Invigilator import models as Invigilator_models
from Restaurant import models as restaurant_models
from Dishes import models as dishes_models

payment_choices = (
	("Cash On Delivery", "Cash On Delivery"),
    ("Online Payment", "Online Payment"),
)

order_status = (
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
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
    delivery_amount = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    discount_amount = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])

    # transaction_id
    status = models.TextField(choices=order_status, null=True, blank=True)
    promocode_used = models.ForeignKey(restaurant_models.RestaurantPromocode, on_delete=models.CASCADE, related_name="orders_order_promocode_used", null=True, blank=True)
    latitude = models.CharField(max_length=30, null=True, blank=True)
    longitude = models.CharField(max_length=30, null=True, blank=True)
    client_address_details = models.TextField(null=True, blank=True)
    delivered_time = models.DateTimeField(null=True, blank=True)

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
    add_ons = models.ManyToManyField(dishes_models.DishAddOns, related_name="orders_order_dish_dish_add_ons", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Order Dish'
        verbose_name_plural = 'Order Dishes'
    def __str__(self):
        return self.dish.name


class IncomingOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orders_incoming_order_order", null=True, blank=True)
    restaurant = models.ForeignKey(restaurant_models.Restaurant, on_delete=models.CASCADE, related_name="orders_incoming_order_restaurant", null=True, blank=True)

    class Meta:
        verbose_name = 'Incoming Order'
        verbose_name_plural = 'Incoming Orders'


class OngoingOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orders_ongoing_order_order", null=True, blank=True)
    restaurant = models.ForeignKey(restaurant_models.Restaurant, on_delete=models.CASCADE, related_name="orders_ongoing_order_restaurant", null=True, blank=True)

    class Meta:
        verbose_name = 'Ongoing Order'
        verbose_name_plural = 'Ongoing Orders'
