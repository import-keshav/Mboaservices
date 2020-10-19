import hashlib, binascii, os

from django.db import models
from django.utils.text import slugify 

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


class User(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    password = models.TextField(null=True, blank=True)
    avatar = models.FileField(upload_to="", null=True, blank=True)
    auth_token = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    def __str__(self):
        return self.name
    def save(self):
        if not self.pk:
            if self.password:
                self.password = hash_password(self.password)
        else:
            obj = User.objects.get(pk=self.pk)
            if obj.password != self.password:
                if self.password:
                    self.password = hash_password(self.password)
        super(User, self).save()


class MobileNumberOTP(models.Model):
    mobile = models.CharField(max_length=15, null=True, blank=True)
    otp = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        verbose_name = 'Mobile Number OTP'
        verbose_name_plural = 'Mobile Number OTPs'
    def __str__(self):
        return self.mobile