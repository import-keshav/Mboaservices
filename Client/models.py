from django.db import models

from User import models as user_Models
# from User import Models as user_Models

class Client(models.Model):
    user = models.ForeignKey(user_Models.User, on_delete=models.CASCADE, related_name="clients", null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    location_coordinates = models.CharField(max_length=30)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class ClientCart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="carts", null=True, blank=True)
    num_of_items = models.IntegerField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = 'ClientCart'
        verbose_name_plural = 'ClientCarts'


class ClientNotification(models.Model):
    client = models.ForeignKey(user_Models.User, on_delete=models.CASCADE, related_name="clientnotificationss", null=True, blank=True)
    notification_text = models.TextField(null=True, blank=True)
    date_time = models.DateTimeField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = 'ClientNotification'
        verbose_name_plural = 'ClientNotifications'
