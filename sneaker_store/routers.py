from rest_framework import routers
from users.views import UserViewSet
from sneakers.views import SneakersViewSet
from purchases.views import PurchasesViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'sneakers', SneakersViewSet, basename='sneakers')
router.register(r'purchases', PurchasesViewSet, basename='purchases')
