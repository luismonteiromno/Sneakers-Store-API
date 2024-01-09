from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token


from .models import UserProfile
from .serializers import UserProfileSerializers


class UserViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers
    permission_classes = AllowAny

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def register_user(self, request):
        data = request.data
        try:
            full_name = data['first_name'] + ' ' + data['last_name']

            user = UserProfile.objects.create(
                username=full_name,
                first_name=data['first_name'],
                full_name=full_name,
                last_name=data['last_name'],
                cpf=data['cpf'],
                email=data['email']
            )

            for favorite_brand in data['favorite_brands']:
                user.favorite_brands.add(int(favorite_brand))
            Token.objects.create(user=user)
            return Response({'message': 'Usuário registrado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao registrar novo usuário!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
