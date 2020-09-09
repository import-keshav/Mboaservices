from django.db import models


class Driver(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    image = models.FileField(null=True, blank=True, upload_to="")

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Restaurant Driver'
        verbose_name_plural = 'Restaurant Drivers'
    def __str__(self):
        return self.name
