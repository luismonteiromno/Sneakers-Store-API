from rest_framework import routers
from users.views import UserViewSet
from sneakers.views import SneakersViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'sneakers', SneakersViewSet, basename='sneakers')
