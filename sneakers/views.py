from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .models import Sneakers, Brands, Lines, Adverts
from .serializers import SneakersSerializers, AdvertsSerializers, BrandsSerializers, LinesSerializers

from users.models import UserProfile

from datetime import datetime


class BrandsViewSet(ModelViewSet):
    queryset = Brands.objects.all()
    serializer_class = BrandsSerializers
    permission_classes = IsAuthenticated

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def register_brand(self, request):
        user = request.user
        data = request.data
        try:
            brand = Brands.objects.create(
                brand_name=data['brand_name']
            )
            for owners in data['owners']:
                owner = UserProfile.objects.get(id=owners)
                if owner.type_user != 'admin':
                    return Response({'message': 'Somente administradores podem ser adicionados!'}, status=status.HTTP_400_BAD_REQUEST)
                brand.owners.add(user)
                brand.owners.add(int(owners))

            return Response({'message': 'Marca registrada com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao adicionar marca!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_brand(self, request):
        user = request.user
        data = request.data
        try:

            brand = Brands.objects.get(pk=data['brand_id'])
            if user.type_user != 'admin':
                return Response({'message': 'Somente administradores podem ser adicionados!'},
                                status=status.HTTP_400_BAD_REQUEST)
            brand.brand_name = data['brand_name']

            if brand.owners != data['owners']:
                for owners in data['owners']:
                    owner = UserProfile.objects.get(id=owners)
                    if owner.type_user != 'admin':
                        return Response({'message': 'Somente administradores podem ser adicionados!'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    brand.owners.add(user)
                    brand.owners.add(int(owners))

            brand.save()
            return Response({'message': 'Marca atualizada com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Marca não encontrada!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao atualizar marca!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_brands(self, request):
        try:
            brands = Brands.objects.all()
            serializer = BrandsSerializers(brands, many=True)
            return Response({'message': 'Marcas encontradas', 'brands': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar marcas!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def brands_by_user(self, request):
        params = request.query_params
        try:
            brands = Brands.objects.get(owners=params['user_id'])
            serializer = BrandsSerializers(brands, many=True)
            return Response({'message': 'Marcas encontradas', 'brands': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Usuário não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar marcas!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def user_brands(self, request):
        user = request.user
        try:
            brands = Brands.objects.filter(owners=user)
            serializer = BrandsSerializers(brands, many=True)
            return Response({'message': 'Marcas encontradas', 'brands': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar marcas!'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'], permission_classes=[AllowAny])
    def exclude_brand(self, request):
        data = request.data
        user = request.user
        try:
            brand = Brands.objects.get(id=data['brand_id'])
            if user not in brand.owners.all():
                return Response({'message': 'Somente administradores podem realizar está ação!'},
                                status=status.HTTP_401_UNAUTHORIZED)
            brand.delete()
            return Response({'message': 'Marca deletada com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Marca não encontrada!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao deletar marca!'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LinesViewSet(ModelViewSet):
    queryset = Lines.objects.all()
    serializer_class = LinesSerializers
    permission_classes = IsAuthenticated

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def register_line(self, request):
        data = request.data
        user = request.user
        try:
            brand = Brands.objects.get(pk=data['brand_id'])
            if user not in brand.owners.all():
                return Response({'message': 'Somente donos/sócios podem realizar está ação!'}, status=status.HTTP_401_UNAUTHORIZED)

            Lines.objects.create(
                brand_line_id=brand.id,
                create_line=data['line_name']
            )
            return Response({'message': 'Linha registrada com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Marca não encontrada!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao registrar linha de tênis!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_line(self, request):
        data = request.data
        user = request.user
        try:
            line = Lines.objects.get(id=data['line_id'])
            if user not in line.brand_line.owners.all():
                return Response({'message': 'Somente donos/sócios podem realizar está ação!'},
                                status=status.HTTP_401_UNAUTHORIZED)
            line.brand_line.id = data['brand_id']
            line.create_line = data['line_name']

            line.save()
            return Response({'message': 'Linha atualizada com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Linha de tênis não encontrada!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao atualizar linha de tênis!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_all_lines(self, request):
        try:
            lines = Lines.objects.all().order_by('id')
            serializer = LinesSerializers(lines, many=True)
            return Response({'message': 'Linhas de tênis encontradas', 'lines': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar linhas de tênis!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def lines_by_brand(self, request):
        params = request.query_params
        try:
            lines = Lines.objects.filter(brand_line_id=params['brand_id'])
            serializer = LinesSerializers(lines, many=True)
            return Response({'message': 'Linhas encontradas', 'lines': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar linhas de tênis!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                    stores_id=data['store_id'],
                    photo=data['photo'],
                    name=data['name'],
                    price=data['price'],
                    brand_id=data['brand_id'],
                    line_id=data.get('line_id', None),
                    model=data['model'],
                    available_sizes=sizes
                )

            else:
                Sneakers.objects.create(
                    stores_id=data['store_id'],
                    photo=data['photo'],
                    name=data['name'],
                    price=data['price'],
                    brand_id=data['brand_id'],
                    line_id=data.get('line_id', None),
                    model=data['model'],
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
