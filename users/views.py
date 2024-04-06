from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from .models import TYPE_USERS
from .models import UserProfile
from .serializers import UserProfileSerializers, UserShoppingCartSerializer

from sneakers.models import Sneakers


class UserViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers
    permission_classes = [AllowAny]
    
    filterset_fields = [
        'first_name',
        'last_name',
        'city',
        'state'
    ]
    
    search_fields = [
        'first_name',
        'last_name',
        'city',
    ]

    # @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    # def register_user(self, request):
    #     data = request.data
    #     try:
    #         full_name = f"{data['first_name']} {data['last_name']}"
    #         phone = data.get('phone', 'Informação não preenchida')
    #         cpf = data['cpf']
    #         if UserProfile.objects.filter(phone=phone).exists():
    #             return Response({'message': 'Este número de telefone já está sendo utilizado!'}, status=status.HTTP_400_BAD_REQUEST)
    #         if UserProfile.objects.filter(cpf=cpf).exists():
    #             return Response({'message': 'Este CPF não é válido!'}, status=status.HTTP_400_BAD_REQUEST)

    #         user = UserProfile.objects.create(
    #             username=full_name,
    #             first_name=data['first_name'],
    #             full_name=full_name,
    #             last_name=data['last_name'],
    #             city=data['city'],
    #             street=data['street'],
    #             state=data['state'],
    #             number_house=data['number_house'],
    #             cep=data['cep'],
    #             complement=data.get('complement', 'informação não preenchida'),
    #             cpf=cpf,
    #             type_user=data['type_user'],
    #             phone=phone,
    #             email=data['email'],
    #             notification_active=data['notification_active']
    #         )

    #         for favorite_brand in data['favorite_brands']:
    #             user.favorite_brands.add(int(favorite_brand))

    #         for favorite_sneaker in data['favorite_sneakers']:
    #             user.favorite_sneakers.add(int(favorite_sneaker))

    #         Token.objects.create(user=user)
    #         return Response({'message': 'Usuário registrado com sucesso'}, status=status.HTTP_200_OK)
    #     except Exception as error:
    #         print(error)
    #         return Response({'message': 'Erro ao registrar novo usuário!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    # def update_user(self, request):
    #     user = request.user
    #     data = request.data
    #     try:
    #         user_update = UserProfile.objects.get(id=user.id)
    #         user_update.username = data['username']
    #         user_update.first_name = data['first_name']
    #         user_update.last_name = data['last_name']
    #         user_update.full_name = data['full_name']
    #         user_update.notification_active = data['notification_active']
    #         user_update.phone = data['phone']
    #         user_update.cep = data['cep']
    #         user_update.city = data['city']
    #         user_update.state = data['state']
    #         user_update.street = data['street']
    #         user_update.number_house = data['number_house']
    #         user_update.complement = data['complement']
    #         user_update.type_user = data['type_user']

    #         if user_update.favorite_brands != data['favorite_brands']:
    #             user_update.favorite_brands.clear()
    #             for favorite_brand in data['favorite_brands']:
    #                 user_update.favorite_brands.add(int(favorite_brand))

    #         if user_update.favorite_sneakers != data['favorite_sneakers']:
    #             user_update.favorite_sneakers.clear()
    #             for favorite_sneaker in data['favorite_sneakers']:
    #                 user_update.favorite_sneakers.add(int(favorite_sneaker))

    #         if user_update.cpf != data['cpf']:
    #             if UserProfile.objects.filter(cpf=data['cpf']).exists():
    #                 return Response({'message': 'CPF inválido!'}, status=status.HTTP_400_BAD_REQUEST)
    #             user_update.cpf = data['cpf']

    #         if user_update.email != data['email']:
    #             if UserProfile.objects.filter(email=data['email']).exists():
    #                 return Response({'message': 'Este email já está sendo utilizado!'}, status=status.HTTP_400_BAD_REQUEST)
    #             user_update.email = data['email']

    #         user_update.save()
    #         return Response({'message': 'Perfil atualizado com sucesso'}, status=status.HTTP_200_OK)
    #     except Exception as error:
    #         print(error)
    #         return Response({'message': 'Erro ao atualizar perfil!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    # def get_user(self, request):
    #     user = request.user
    #     try:
    #         user = UserProfile.objects.get(id=user.id)
    #         serializer = UserProfileSerializers(user)
    #         return Response({'message': 'Usuário encontrado', 'user': serializer.data}, status=status.HTTP_200_OK)
    #     except Exception as error:
    #         print(error)
    #         return Response({'message': 'Erro ao exibir perfil do usuário!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    # def user_by_id(self, request):
    #     params = request.query_params
    #     try:
    #         user = UserProfile.objects.get(id=params['user_id'])
    #         serializer = UserProfileSerializers(user)
    #         return Response({'message': 'Usuário encontrado', 'user': serializer.data}, status=status.HTTP_200_OK)
    #     except Exception as error:
    #         print(error)
    #         return Response({'message': 'Erro ao exibir perfil do usuário!'},
    #                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(detail=False, methods=['DELETE'], permission_classes=[IsAuthenticated])
    # def delete_user(self, request):
    #     user = request.user
    #     try:
    #         user = UserProfile.objects.get(id=user.id)
    #         user.delete()
    #         return Response({'message': 'Usuário deletado com sucesso'}, status=status.HTTP_200_OK)
    #     except Exception as error:
    #         print(error)
    #         return Response({'message': 'Erro ao deletar usuário!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    # def types_of_user(self, request):
    #     try:
    #         types = []
    #         for type_owners in TYPE_USERS:
    #             types.append(type_owners[1])
    #         return Response({'message': 'Tipos de usuário', 'types': types}, status=status.HTTP_200_OK)
    #     except Exception as error:
    #         print(error)
    #         return Response({'message': 'Erro ao listar tipos de usuários!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    # def add_product_cart(self, request):
    #     user = request.user
    #     data = request.data
    #     try:
    #         for sneaker in data['sneakers']:
    #             if not Sneakers.objects.filter(id=sneaker).exists():
    #                 return Response({'message': 'Produto não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
    #             products = Sneakers.objects.get(id=sneaker)
    #             user.shopping_cart.add(products)
    #         return Response({'message': 'Produto adicionado com sucesso'}, status=status.HTTP_200_OK)
    #     except Exception as error:
    #         print(error)
    #         return Response({'message': 'Erro ao adicionar produtos ao carrinho de compra'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    # def products_of_shopping_cart(self, request):
    #     user = request.user
    #     try:
    #         user_cart = UserProfile.objects.get(pk=user.id)
    #         serializer = UserShoppingCartSerializer(user_cart).data
    #         return Response({'message': 'Carrinho de compras', 'shopping_cart': serializer}, status=status.HTTP_200_OK)
    #     except Exception as error:
    #         print(error)
    #         return Response({'message': 'Erro ao listar produtos ao carrinho de compra'})
