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

                if data['delivery'] == True and (
                        data['minimum_delivery'] in invalids_values or data['maximum_delivery'] in invalids_values
                ):
                    return Response({'message': 'O campo tempo minímo/máximo de entrega deve ser preenchido!'}, status=status.HTTP_400_BAD_REQUEST)

                if data['delivery'] == False and (
                        data['minimum_delivery'] not in invalids_values or data['maximum_delivery'] not in invalids_values
                ):
                    return Response({'message': 'Preencha o campo de Entrega que os campos de tempo minímo/máximo de entrega possa(m) ser preenchido(s)!'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if data['minimum_delivery'] not in invalids_values and data['maximum_delivery'] not in invalids_values and (
                        data['minimum_delivery'] >= data['maximum_delivery']
                ):
                    return Response({'message': 'Preencha o campo tempo minímo/máximo de entrega corretamente!'}
                                    , status=status.HTTP_400_BAD_REQUEST)

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
                    delivery=data['delivery'],
                    minimum_delivery=data['minimum_delivery'],
                    maximum_delivery=data['maximum_delivery']
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

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_store(self, request):
        user = request.user
        data = request.data
        try:
            invalids_values = [None, ' ', '']
            store = Store.objects.get(id=data['store_id'])
            if user in store.owner.all():
                store.name = data['name']
                store.street = data['street']
                store.number = data['number']
                store.state = data['state']

                if data['cnpj'] != store.cnpj:
                    if Store.objects.filter(cnpj=data['cnpj']).exists():
                        return Response({'message': 'Este CNPJ já está sendo utilizado!'}, status=status.HTTP_400_BAD_REQUEST)
                    store.cnpj = data['cnpj']

                if data['email'] != store.email:
                    if Store.objects.filter(email=data['email']).exists():
                        return Response({'message': 'Este EMAIL já está sendo utilizado!'}, status=status.HTTP_400_BAD_REQUEST)
                    store.email = data['email']

                store.facebook = data.get('facebook', None)
                store.instagram = data.get('instagram', None)
                store.whatsapp = data.get('whatsapp', None)

                if data['owners'] != store.owner:
                    store.owner.clear()
                    for owner in data['owners']:
                        store.owner.add(owner)

                if data['products'] != store.products:
                    store.products.clear()
                    for product in data['products']:
                        store.products.add(product)

                if data['type_payments'] != store.type_payments:
                    store.type_payments.clear()
                    for type_payment in data['type_payments']:
                        store.type_payments.add(type_payment)

                store.delivery = data['delivery']
                store.minimum_delivery = data['minimum_delivery']
                store.maximum_delivery = data['maximum_delivery']

                if data['delivery'] == True and (
                        data['minimum_delivery'] in invalids_values or data['maximum_delivery'] in invalids_values
                ):
                    return Response({'message': 'O campo tempo minímo/máximo de entrega deve ser preenchido!'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if data['delivery'] == False and (
                        data['minimum_delivery'] not in invalids_values or data['maximum_delivery'] not in invalids_values
                ):
                    return Response({
                                        'message': 'Preencha o campo de Entrega que os campos de tempo minímo/máximo de entrega possa(m) ser preenchido(s)!'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if data['minimum_delivery'] not in invalids_values and data['maximum_delivery'] not in invalids_values and (
                        data['minimum_delivery'] >= data['maximum_delivery']
                ):
                    return Response({'message': 'Preencha o campo tempo minímo/máximo de entrega corretamente!'}
                                    , status=status.HTTP_400_BAD_REQUEST)

                store.save()
                return Response({'message': 'Loja atualizada com sucesso'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Somente o(s) dono(s) pode(m) realizar esta ação!'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao atualizar dados da loja!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
