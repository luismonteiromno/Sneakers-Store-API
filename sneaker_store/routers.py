from rest_framework import routers
from users.views import UserViewSet
from store.views import StoreViewSet
from sneakers.views import SneakersViewSet
from purchases.views import PurchasesViewSet
from type_payments.views import TypePaymentsViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'stores', StoreViewSet, basename='stores')
router.register(r'sneakers', SneakersViewSet, basename='sneakers')
router.register(r'purchases', PurchasesViewSet, basename='purchases')
router.register(r'type_payments', TypePaymentsViewSet, basename='type_payments')
