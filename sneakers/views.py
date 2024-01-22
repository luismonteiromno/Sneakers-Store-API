from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .models import Sneakers, Brands, Lines, Adverts
from .serializers import SneakersSerializers, AdvertsSerializers

from datetime import datetime

class SneakersViewSet(ModelViewSet):
    queryset = Sneakers.objects.all()
    serializer_class = SneakersSerializers
    permission_classes = IsAuthenticated

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def register_sneaker(self, request):
        data = request.data
        try:
            available_sizes = data['available_sizes'].split(",")
            sizes = []

            for available_size in available_sizes:
                sizes.append(available_size)

            invalids = [None, ' ', '']
            if data.get('line_id') not in invalids:
                brand = Brands.objects.get(id=data['brand_id'])
                line = Lines.objects.get(id=data.get('line_id'))

                if line.brand_line != brand:
                    return Response({'message': 'A linha escolhida não pertence a essa marca!'},
                                    status=status.HTTP_400_BAD_REQUEST)

                Sneakers.objects.create(
                    photo=data['photo'],
                    name=data['name'],
                    price=data['price'],
                    brand_id=data['brand_id'],
                    line_id=data.get('line_id', None),
                    model=data['model'],
                    in_stock=data['in_stock'],
                    available_sizes=sizes
                )

            else:
                Sneakers.objects.create(
                    photo=data['photo'],
                    name=data['name'],
                    price=data['price'],
                    brand_id=data['brand_id'],
                    line_id=data.get('line_id', None),
                    model=data['model'],
                    in_stock=data['in_stock'],
                    available_sizes=sizes
                )

            return Response({'message': 'Tênis registrado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao registrar tênis!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_sneaker(self, request):
        data = request.data
        available_sizes = data['available_sizes'].split(",")
        sizes = []
        try:
            invalids = [None, ' ', '']
            if data.get('line_id') not in invalids:
                brand = Brands.objects.get(id=data['brand_id'])
                line = Lines.objects.get(id=data.get('line_id'))

                if line.brand_line != brand:
                    return Response({'message': 'A linha escolhida não pertence a essa marca!'},
                                    status=status.HTTP_400_BAD_REQUEST)
                sneaker = Sneakers.objects.get(id=data['sneaker_id'])
                sneaker.photo = data['photo']
                sneaker.name = data['name']
                sneaker.price = data['price']
                sneaker.brand_id = data['brand_id']
                sneaker.line_id = data.get('line_id')
                sneaker.model = data['model']
                sneaker.in_stock = data['in_stock']
                if sneaker.available_sizes != available_sizes:
                    sneaker.available_sizes.clear()
                    for available_size in available_sizes:
                        sizes.append(available_size)
                        sneaker.available_sizes = sizes

                sneaker.save()
            else:
                sneaker = Sneakers.objects.get(id=data['sneaker_id'])
                sneaker.photo = data['photo']
                sneaker.name = data['name']
                sneaker.price = data['price']
                sneaker.brand_id = data['brand_id']
                sneaker.line_id = data.get('line_id')
                sneaker.model = data['model']
                sneaker.in_stock = data['in_stock']
                if sneaker.available_sizes != available_sizes:
                    sneaker.available_sizes.clear()
                    for available_size in available_sizes:
                        sizes.append(available_size)
                        sneaker.available_sizes = sizes

                sneaker.save()
            return Response({'message': 'Tênis atualizado com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Tênis não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao atualizar tênis!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_sneakers(self, request):
        try:
            sneakers = Sneakers.objects.all()
            serializer = SneakersSerializers(sneakers, many=True)
            return Response({'message': 'Tênis encontrados', 'sneakers': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar os tênis!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def sneaker_by_id(self, request):
        params = request.query_params
        try:
            sneakers = Sneakers.objects.get(id=params['sneaker_id'])
            serializer = SneakersSerializers(sneakers)
            return Response({'message': 'Tênis encontrado', 'sneaker': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Tênis não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao buscas o tênis!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def delete_sneaker(self, request):
        data = request.data
        user = request.user
        try:
            sneaker = Sneakers.objects.get(pk=data['sneaker_id'])
            if user not in sneaker.brand.owners.all():
                return Response({'message': 'Somente donos/sócios podem deletar este produto!'}, status=status.HTTP_403_FORBIDDEN)
            sneaker.delete()
            return Response({'message': 'Tênis deletado com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Tênis não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao deletar tênis'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdvertsViewSet(ModelViewSet):
    queryset = Adverts.objects.all()
    serializer_class = AdvertsSerializers
    permission_classes = AllowAny

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def create_advert(self, request):
        data = request.data
        try:
            create_at = datetime.strptime(data['create_at'], '%d/%m/%Y %H:%M')
            expiration = datetime.strptime(data['expiration'], '%d/%m/%Y %H:%M')
            if create_at >= expiration:
                return Response({'message': 'A data de criação não pode ser maior/igual a data de expiração!'}, status=status.HTTP_400_BAD_REQUEST)
            advert = Adverts.objects.create(
                advert=data['advert'],
                description=data['description'],
                create_at=create_at,
                expiration=expiration
            )
            for sneaker in data['sneakers'].split(','):
                advert.sneaker.add(sneaker)

            return Response({'message': 'Anúncio criado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao criar anúncio!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_adverts(self, request):
        now = datetime.now()
        try:
            adverts = Adverts.objects.filter(create_at__lte=now, expiration__gte=now)
            serializer = AdvertsSerializers(adverts, many=True)
            return Response({'message': 'Anúncios encontrados', 'adverts': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar anúncios'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
