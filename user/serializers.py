from . import models

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'slug', 
            'name', 
            'created', 
            'last_updated', 
            'email', 
            'mobile', 
            'password', 
            'avatar', 
        )


