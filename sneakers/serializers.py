from rest_framework import serializers
from .models import Sneakers, Adverts, Brands, Lines


class BrandsSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Brands
        fields = '__all__'


class LinesSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Lines
        fields = '__all__'


class SneakersSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 3
        model = Sneakers
        fields = '__all__'


class AdvertsSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Adverts
        fields = '__all__'
