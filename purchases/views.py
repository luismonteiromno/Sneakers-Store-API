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

