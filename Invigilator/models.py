from django.db import models
from django.core.validators import MinValueValidator

from User import models as user_models
from Client import models as client_models
from Restaurant import models as restaurant_models
from Orders import models as order_models

choices = (
    ('Client', 'Client'),
    ('Invigilator', 'Invigilator')
)

class Invigilator(models.Model):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="invigilator_invigilator_user", null=True, blank=True)
    city =  models.CharField(max_length=100, null=True, blank=True)
    latitude = models.CharField(max_length=30, null=True, blank=True)
    longitude = models.CharField(max_length=30, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Invigilator'
        verbose_name_plural = 'Invigilators'
    def __str__(self):
        return self.user.name


class InvigilatorRestaurant(models.Model):
    invigilator = models.ForeignKey(Invigilator, on_delete=models.CASCADE, related_name="invigilator_invigilator_restaurant_invigilator", null=True, blank=True)
    restaurant = models.ForeignKey(restaurant_models.Restaurant, on_delete=models.CASCADE, related_name="invigilator_invigilator_restaurant_restaurant", null=True, blank=True)

    class Meta:
        verbose_name = 'Invigilator Restaurant'
        verbose_name_plural = 'Invigilator Restaurants'


class InvigilatorClientMessage(models.Model):
    invigilator = models.ForeignKey(Invigilator, on_delete=models.CASCADE, related_name="invigilator_invigilator_client_chat_invigilator", null=True, blank=True)
    client = models.ForeignKey(client_models.Client, on_delete=models.CASCADE, related_name="invigilator_invigilator_client_chat_client", null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    message_from = models.TextField(choices=choices, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Invigilator Client Message'
        verbose_name_plural = 'Invigilator Client Message'
    def __str__(self):
        if self.invigilator.user:
            return self.invigilator.user.name
        return ''
