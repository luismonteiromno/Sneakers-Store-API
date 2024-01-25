from django.contrib import admin
from .models import Purchases


class PurchasesAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_purchase']


admin.site.register(Purchases, PurchasesAdmin)

