from rest_framework import serializers

from . import models
class DriverGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Driver
        fields = '__all__'