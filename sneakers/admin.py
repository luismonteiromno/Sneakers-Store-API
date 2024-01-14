from django.contrib import admin
from .models import Sneakers, Brands, Lines, Adverts


class BrandsAdmin(admin.ModelAdmin):
    filter_horizontal = ['owners']


class SneakersAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand']
    list_filter = ['brand', 'line', 'in_stock']


class AdvertsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informações do anúncio', {'fields': ('sneaker', 'advert', 'create_at', 'expiration')}),
    )
    list_display = ['sneaker', 'create_at', 'expiration']


admin.site.register(Sneakers, SneakersAdmin)
admin.site.register(Brands, BrandsAdmin)
admin.site.register(Lines)
admin.site.register(Adverts, AdvertsAdmin)
