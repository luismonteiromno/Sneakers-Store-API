from django.contrib import admin
from .models import Sneakers, Brands, Lines, Adverts
from django import forms
from django.forms import ValidationError


class BrandsAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand_name']
    filter_horizontal = ['owners']


class LinesAdmin(admin.ModelAdmin):
    list_display = ['id', 'create_line']


class SneakersAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand']
    list_filter = ['brand', 'line', 'in_stock']


class AdvertsForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        create_at = cleaned_data.get('create_at')
        expiration = cleaned_data.get('expiration')
        if create_at >= expiration:
            raise ValidationError('A data de criação não pode ser maior/igual a data de expiração!')


class AdvertsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informações do anúncio', {'fields': ('sneaker', 'advert', 'description', 'create_at', 'expiration')}),
    )
    list_display = ['id', 'create_at', 'expiration']
    filter_horizontal = ['sneaker']
    form = AdvertsForm


admin.site.register(Sneakers, SneakersAdmin)
admin.site.register(Brands, BrandsAdmin)
admin.site.register(Lines, LinesAdmin)
admin.site.register(Adverts, AdvertsAdmin)
