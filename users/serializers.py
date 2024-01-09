from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
