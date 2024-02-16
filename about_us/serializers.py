from rest_framework.serializers import ModelSerializer
from .models import AboutUs, TermsOfUse


class AboutUsSerializer(ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'


class TermsOfUseSerializer(ModelSerializer):
    class Meta:
        model = TermsOfUse
        fields = '__all__'
