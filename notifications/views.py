from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from .models import Notifications

from .serializers import NotificationsSerializers


class NotificationsViewSet(ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializers
    permission_classes = AllowAny

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_notifications(self, request):
        try:
            notifications = self.queryset
            serializer = NotificationsSerializers(notifications, many=True)
            return Response({'message': 'Notificações encontradas', 'notifications': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
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
