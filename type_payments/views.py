from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from .models import TypePayments
from .serializers import TypePaymentsSerializers


class TypePaymentsViewSet(ModelViewSet):
    queryset = TypePayments.objects.all()
    serializer_class = TypePaymentsSerializers
    permission_classes = IsAuthenticated

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def register_type_payment(self, request):
        data = request.data
        try:
            TypePayments.objects.create(
                payment=data['new_payment']
            )
            return Response({'message': 'Novo tipo de pagamento registrado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'erro'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_type_payments(self, request):
        try:
            payments = TypePayments.objects.all()
            serializer = TypePaymentsSerializers(payments, many=True)
            return Response({'message': 'Tipos de pagamentos encontrados', 'payments': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar tipos de pagamentos'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
