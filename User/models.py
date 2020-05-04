from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=15)
    password = models.TextField(null=True, blank=True)
    avatar = models.FileField(upload_to="")

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
