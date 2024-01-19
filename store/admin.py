from django.contrib import admin
from .models import Store


class StoreAdmin(admin.ModelAdmin):
    filter_horizontal = ['owner', 'products', 'type_payments']


admin.site.register(Store, StoreAdmin)
