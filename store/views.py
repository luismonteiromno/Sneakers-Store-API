from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action


from .models import Store
from .serializers import StoreSerializers


class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializers
    permission_classes = IsAuthenticated

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def register_store(self, request):
        data = request.data
        user = request.user
        try:
            if user.type_user == 'admin':
                invalids_values = [None, ' ', '']
                if Store.objects.filter(email=data['email']).exists():
                    return Response({'message': 'Este email já está sendo utilizado!'}, status=status.HTTP_400_BAD_REQUEST)

                if Store.objects.filter(cnpj=data['cnpj']).exists():
                    return Response({'message': 'Este CNPJ pertence não existe ou pertence a outra empresa!'}, status=status.HTTP_400_BAD_REQUEST)

                store = Store.objects.create(
                    name=data['name'],
                    street=data['street'],
                    number=data['number'],
                    state=data['state'],
                    cnpj=data['cnpj'],
                    email=data['email'],
                    facebook=data.get('facebook'),
                    instagram=data.get('instagram'),
                    whatsapp=data.get('whatsapp'),
                )
                if data['owners'] not in invalids_values:
                    for owner in data['owners']:
                        store.owner.add(owner)
                else:
                    return Response({'message': 'Há um valor inválido no registro do(s) dono(s)!'}, status=status.HTTP_400_BAD_REQUEST)

                if data['products'] not in invalids_values:
                    for product in data['products']:
                        store.products.add(product)
                else:
                    return Response({'message': 'Há um valor inválido no registro de produtos!'}, status=status.HTTP_400_BAD_REQUEST)

                if data['type_payments'] not in invalids_values:
                    for type_payment in data['type_payments']:
                        store.type_payments.add(type_payment)
                else:
                    return Response({'message': 'Há um valor inválido no registro de tipos de pagamentos!'}, status=status.HTTP_400_BAD_REQUEST)

                return Response({'message': 'Loja registrada com sucesso'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Somente usuários admins podem realizar está ação!'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao registrar loja!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def user_stores(self, request):
        user = request.user
        try:
            stores = Store.objects.filter(owner=user)
            serializer = StoreSerializers(stores, many=True)
            return Response({'message': 'Loja(s) em que o usuário é dono', 'stores': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listas lojas!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
