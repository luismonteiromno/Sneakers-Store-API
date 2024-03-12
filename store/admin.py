from django.contrib import admin
from .models import Store
from django import forms
from django.forms import ValidationError

from users.models import UserProfile


class StoreForm(forms.ModelForm):
    def clean(self):
        invalids = [None, ' ', '']
        cleaned_data = super().clean()
        opening_time = cleaned_data.get('opening_time')
        closing_time = cleaned_data.get('closing_time')
        delivery = cleaned_data.get('delivery')
        minimum_delivery = cleaned_data.get('minimum_delivery')
        maximum_delivery = cleaned_data.get('maximum_delivery')

        if opening_time >= closing_time:
            raise ValidationError('O horário de encerramento não pode ser maior/igual ao de abertura')

        if delivery == True and (
                minimum_delivery in invalids or maximum_delivery in invalids
        ):
            raise ValidationError('O campo tempo minímo/máximo de entrega deve ser preenchido!')

        if delivery == False and (
                minimum_delivery not in invalids or maximum_delivery not in invalids
        ):
            raise ValidationError('Preencha o campo de Entrega que os campos de tempo minímo/máximo de entrega possa(m) ser preenchido(s)!')

        if minimum_delivery not in invalids and maximum_delivery not in invalids and (
                minimum_delivery >= maximum_delivery
        ):
            raise ValidationError('Preencha o campo tempo minímo/máximo de entrega corretamente!')


class StoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    filter_horizontal = ['owner', 'employees', 'products', 'type_payments', 'orders']
    form = StoreForm

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'employees':
            kwargs['queryset'] = UserProfile.objects.filter(type_user='employee')
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Store, StoreAdmin)
