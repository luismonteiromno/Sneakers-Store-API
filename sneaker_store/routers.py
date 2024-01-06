from rest_framework import routers
from sneakers.views import SneakersViewSet

router = routers.DefaultRouter()

router.register(r'sneakers', SneakersViewSet, basename='sneakers')
