from rest_framework import serializers
from .models import Sneakers


class SneakersSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Sneakers
        fields = '__all__'
