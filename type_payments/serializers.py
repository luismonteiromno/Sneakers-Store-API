from rest_framework import serializers
from .models import TypePayments


class TypePaymentsSerializers(serializers.ModelSerializer):

    class Meta:
        model = TypePayments
        fields = '__all__'
