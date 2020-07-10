from django.db import models
from django.core.validators import MinValueValidator

from User import models as user_models
from Orders import models as order_models


class Invigilator(models.Model):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="invigilator_invigilator_user", null=True, blank=True)
    location_coordinates = models.CharField(max_length=30, null=True, blank=True)
    city =  models.CharField(max_length=100, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Invigilator'
        verbose_name_plural = 'Invigilators'
    def __str__(self):
        return self.user.name


class InvigilatorOrderAssignment(models.Model):
    invigilator = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="invigilator_invigilator_order_assignment_invigilator", null=True, blank=True)
    order = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="invigilator_invigilator_order_assignment_order", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Invigilator Order Assignment'
        verbose_name_plural = 'Invigilator Order Assignments'
    def __str__(self):
        return self.invigilator
