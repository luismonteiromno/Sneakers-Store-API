from rest_framework import serializers
from .models import Purchases


class PurchasesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields = '__all__'
