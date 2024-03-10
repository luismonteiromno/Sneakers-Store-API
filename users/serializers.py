from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializers(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()

    # def get_phone(self, obj):
    #     invalids = [None, ' ', '']
    #     if obj.phone in invalids:
    #         obj.phone = 'Campo não preenchido'
    #         return obj.phone
    #     else:
    #         return obj.phone

    class Meta:
        model = UserProfile
        fields = '__all__'
