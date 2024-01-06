from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .models import Sneakers
from .serializers import SneakersSerializers


class SneakersViewSet(ModelViewSet):
    queryset = Sneakers.objects.all()
    serializer_class = SneakersSerializers
    permission_classes = IsAuthenticated

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_sneakers(self, request):
        try:
            sneakers = Sneakers.objects.all()
            serializer = SneakersSerializers(sneakers, many=True)
            return Response({'message': 'Tênis encontrados', 'sneakers': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar os tênis!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)