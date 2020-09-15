import hashlib, binascii, os

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from User import models as user_models


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


class RestraurantDishesCategory(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Restraurant Dishes Category'
        verbose_name_plural = 'Restraurant Dishes Categories'
    def __str__(self):
        return self.name


class Restaurant(models.Model):
    unique_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    password = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True, upload_to="")
    address = models.TextField(null=True, blank=True) 
    latitude = models.CharField(max_length=30, null=True, blank=True)
    longitude = models.CharField(max_length=30, null=True, blank=True)
    category = models.ManyToManyField(RestraurantDishesCategory, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    is_open = models.BooleanField(default=False, null=True, blank=True)

    auth_token = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'
    def __str__(self):
        return self.name
    def save(self):
        self.password = hash_password(self.password)
        super(Restaurant, self).save()


class RestaurantEmployee(models.Model):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="user", null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_restaurant_employee_restaurant", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Restaurant Employee'
        verbose_name_plural = 'Restaurant Employees'
    def __str__(self):
        return self.user.name


class RestaurantPromocode(models.Model):
    promocode = models.CharField(max_length=10, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_restaurant_promocode_restaurant", null=True, blank=True)
    discount_percentage = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    valid_date = models.DateField(null=True, blank=True)
    category = models.ManyToManyField(RestraurantDishesCategory)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Restaurant Promocode'
        verbose_name_plural = 'Restaurant Promocodes'
    def __str__(self):
        return self.promocode


class GlobalPromocode(models.Model):
    promocode = models.CharField(max_length=10, null=True, blank=True)
    discount_percentage = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    valid_date = models.DateField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        verbose_name = 'Global Promocode'
        verbose_name_plural = 'Global Promocodes'
    def __str__(self):
        return self.promocode
