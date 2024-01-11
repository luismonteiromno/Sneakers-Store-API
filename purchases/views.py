from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Purchases
from users.models import UserProfile
from sneakers.models import Sneakers
from .serializers import PurchasesSerializers

from datetime import datetime


class PurchasesViewSet(ModelViewSet):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializers
    permission_classes = IsAuthenticated

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def register_purchase(self, request):
        now = datetime.now()
        user = request.user
        data = request.data
        try:
            purchase = Purchases.objects.create(
                user_id=user.id,
                date_purchase=now
            )
            for sneaker in data['sneakers']:
                purchase.sneaker.add(int(sneaker))
            return Response({'message': 'Compra efetuada com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao realizar compra!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def purchases_by_user(self, request):
        user = request.user
        try:
            purchases = Purchases.objects.filter(user=user)
            serializer = PurchasesSerializers(purchases, many=True)
            return Response({'message': 'Compras encontradas', 'purchases': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar compras do usuário!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def purchase_by_id(self, request):
        params = request.query_params
        try:
            purchase = Purchases.objects.get(pk=params['purchase_id'])
            serializer = PurchasesSerializers(purchase)
            return Response({'message': 'Compra encontrada', 'purchase': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Compra não encontrada!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao buscar registro de compra!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)