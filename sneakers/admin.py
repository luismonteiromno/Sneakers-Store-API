from django.contrib import admin
from .models import Sneakers, Brands, Lines

class SneakersAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand']


admin.site.register(Sneakers, SneakersAdmin)
admin.site.register(Brands)
admin.site.register(Lines)
