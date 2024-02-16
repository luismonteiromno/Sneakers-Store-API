from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from .models import AboutUs, TermsOfUse

from .serializers import AboutUsSerializer, TermsOfUseSerializer

from datetime import datetime
import sentry_sdk


class AboutUsViewSet(ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = AllowAny

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def about_us(self, request):
        try:
            about_us = AboutUs.objects.last()
            if about_us != None:
                serializer = AboutUsSerializer(about_us)
                return Response({'message': 'Sobre nós', 'about_us': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Nenhuma informação encontrada!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao exibir sobre nós!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
