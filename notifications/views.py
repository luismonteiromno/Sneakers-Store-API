from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from .models import Notifications

from users.models import UserProfile

from .serializers import NotificationsSerializers

from datetime import datetime
import sentry_sdk


class NotificationsViewSet(ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializers
    permission_classes = AllowAny

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def send_notification(self, request):
        data = request.data
        now = datetime.now()
        try:
            email = data['email']
            if UserProfile.objects.filter(email=email).exists():
                Notifications.objects.create(
                    email=email,
                    subject=data['subject'],
                    message=data['message'],
                    send_date=now
                )
                return Response({'message': 'Notificação enviada com sucesso'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Email não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao enviar notificação!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_notifications(self, request):
        try:
            notifications = Notifications.objects.all()
            serializer = NotificationsSerializers(notifications, many=True)
            return Response({'message': 'Notificações encontradas', 'notifications': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar notificações'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PUT'], permission_classes=[IsAuthenticated])
    def read_notification(self, request):
        data = request.data
        try:
            notification = Notifications.objects.get(id=data['notification_id'])
            notification.is_read = data['is_read']
            notification.save()
            return Response({'message': 'Notificação lida com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao ler notificação!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def notifications_by_user(self, request):
        user = request.user
        try:
            notifications = Notifications.objects.filter(email=user.email)
            serializer = NotificationsSerializers(notifications, many=True)
            return Response({'message': 'Notificações encontradas', 'notifications': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar notificações!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def notifications_purchases(self, request):
        try:
            notifications = list(Notifications.objects.filter(purchase_notification=True))
            if notifications == []:
                return Response({'message': 'Nenhuma notificação encontrada!'}, status=status.HTTP_200_OK)
            serializer = NotificationsSerializers(notifications, many=True)
            return Response({'message': 'Notificações encontradas', 'notifications': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar notificações de compras!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
