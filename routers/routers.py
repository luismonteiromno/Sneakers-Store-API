from rest_framework import routers
from users.views import UserViewSet
from store.views import StoreViewSet
from sneakers.views import SneakersViewSet, AdvertsViewSet, BrandsViewSet, LinesViewSet
from purchases.views import PurchasesViewSet
from type_payments.views import TypePaymentsViewSet
from notifications.views import NotificationsViewSet
from about_us.views import AboutUsViewSet, TermsOfUseViewSet, PrivacyPolicyViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'stores', StoreViewSet, basename='stores')
router.register(r'sneakers', SneakersViewSet, basename='sneakers')
router.register(r'brands', BrandsViewSet, basename='brands')
router.register(r'lines', LinesViewSet, basename='lines')
router.register(r'adverts', AdvertsViewSet, basename='adverts')
router.register(r'purchases', PurchasesViewSet, basename='purchases')
router.register(r'type_payments', TypePaymentsViewSet, basename='type_payments')
router.register(r'notifications', NotificationsViewSet, basename='notifications')
router.register(r'about_us', AboutUsViewSet, basename='about_us')
router.register(r'terms_of_use', TermsOfUseViewSet, basename='terms_of_use')
router.register(r'privacy_police', PrivacyPolicyViewSet, basename='privacy_police')
