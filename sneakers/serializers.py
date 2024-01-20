from rest_framework import serializers
from .models import Sneakers, Adverts


class SneakersSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Sneakers
        fields = '__all__'


class AdvertsSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Adverts
        fields = '__all__'
