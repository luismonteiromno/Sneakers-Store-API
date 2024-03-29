from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from .models import AboutUs, TermsOfUse, PrivacyPolicy

from .serializers import AboutUsSerializer, TermsOfUseSerializer, PrivacyPoliceSerializer

from datetime import datetime
import sentry_sdk


class AboutUsViewSet(ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [AllowAny]

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


class TermsOfUseViewSet(ModelViewSet):
    queryset = TermsOfUse.objects.all()
    serializer_class = TermsOfUseSerializer
    permission_classes = AllowAny

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def terms_of_use(self, request):
        try:
            terms_of_use = TermsOfUse.objects.last()
            if terms_of_use != None:
                serializer = TermsOfUseSerializer(terms_of_use)
                return Response({'message': 'Termos de Uso', 'terms_of_use': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Nenhuma informação encontrada!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao exibir termos de uso!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PrivacyPolicyViewSet(ModelViewSet):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPoliceSerializer
    permission_classes = [AllowAny]
    
    filterset_fields = [
        'privacy_policy'
    ]

    # @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    # def privacy_police(self, request):
    #     try:
    #         privacy_police = PrivacyPolicy.objects.last()
    #         if privacy_police != None:
    #             serializer = PrivacyPoliceSerializer(privacy_police)
    #             return Response({'message': 'Politica de Privacidade', 'privacy_police': serializer.data},
    #                             status=status.HTTP_200_OK)
    #         else:
    #             return Response({'message': 'Nenhuma informação encontrada!'}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as error:
    #         print(error)
    #         return Response({'message': 'Erro ao exibir politica de privacidade!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
