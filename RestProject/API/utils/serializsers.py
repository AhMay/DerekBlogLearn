from rest_framework import serializers
from API import models


class PagerSerialiser(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = "__all__"