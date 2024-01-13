from django.contrib import admin
from .models import Sneakers, Brands, Lines


class BrandsAdmin(admin.ModelAdmin):
    filter_horizontal = ['owners']


class SneakersAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand']
    list_filter = ['brand', 'line', 'in_stock']


admin.site.register(Sneakers, SneakersAdmin)
admin.site.register(Brands, BrandsAdmin)
admin.site.register(Lines)
