from rest_framework import serializers
from .models import Store


class StoreSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Store
        fields = '__all__'
