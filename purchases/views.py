from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Purchases
from users.models import UserProfile
from sneakers.models import Sneakers
from .serializers import PurchasesSerializers
from notifications.models import Notifications

from type_payments.models import TypePayments

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
        total_purchase_price = 0
        try:
            try:
                type_payment = TypePayments.objects.get(id=data['type_payment'])
            except Exception as error_payment:
                print(error_payment)
                return Response({'message': 'Tipo de pagamento não encontrado!'}, status=status.HTTP_404_NOT_FOUND)

            purchase = Purchases.objects.create(
                user_id=user.id,
                date_purchase=now,
                type_payment_id=type_payment.id,
            )

            for sneaker_id in data['sneakers']:
                sneaker = Sneakers.objects.get(id=sneaker_id)
                price = sneaker.price

                if data['sneaker_size'] not in sneaker.available_sizes:
                    return Response({'message': 'O tamanho selecionado não está disponível!'}, status=status.HTTP_400_BAD_REQUEST)

                if type_payment not in sneaker.stores.type_payments.all():
                    return Response({'message': 'Esse tipo de pagamento não é aceito pela loja!'}, status=status.HTTP_403_FORBIDDEN)

                if sneaker.in_stock == False:
                    return Response({'message': 'Um dos tênis escolhidos não está em estoque!'}, status=status.HTTP_400_BAD_REQUEST)

                if user.type_user == 'employee':
                    price -= price * 0.15
                    total_purchase_price += price
                    purchase.total_purchase = total_purchase_price
                    purchase.employee_discount = True

                else:
                    total_purchase_price += sneaker.price
                    purchase.total_purchase = total_purchase_price

                    purchase.sneaker_size = data['sneaker_size']
                    purchase.sneaker.add(sneaker.id)
                    purchase.save()

            for sneaker in data['sneakers']:
                sneakers = Sneakers.objects.get(id=sneaker)
                for owner in sneakers.stores.owner.all():
                    Notifications.objects.create(
                        email=owner.email,
                        subject='Nova compra realizada',
                        message=f'O(s) produto(s) {sneakers} foi(ram) comprado(s)!',
                        purchase_notification=True
                    )

            return Response({'message': 'Compra efetuada com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Algum dos tênis escolhidos não foi/foram encontrado(s)!'}, status=status.HTTP_404_NOT_FOUND)
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

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def purchases_with_discount(self, request):
        try:
            purchases = Purchases.objects.filter(employee_discount=True)
            serializer = PurchasesSerializers(purchases, many=True)
            return Response({'message': 'Compras encontradas', 'purchases': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar compras!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
