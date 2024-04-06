from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin


class UserProfileAdmin(UserAdmin):
    fieldsets = (
        ('Informações Pessoais', {'fields': ('username', 'first_name', 'last_name', 'cpf', 'email', 'phone', 'type_user')}),
        ('Localização', {'fields': ('city', 'cep', 'street', 'number_house', 'complement', 'state')}),
        ('Informações de Notificações', {'fields': ('favorite_brands', 'favorite_sneakers', 'shopping_cart', 'notification_active')}),
        ('Informações do Usuário', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')})
    )
    list_display = ['id', 'username', 'email', 'type_user']
    search_fields = ['username', 'first_name', 'last_name']
    filter_horizontal = ['favorite_brands', 'favorite_sneakers', 'shopping_cart', 'groups', 'user_permissions']
    list_filter = ['type_user']

    def save_model(self, request, obj, form, change):
        full_name = obj.first_name + ' ' + obj.last_name
        obj.full_name = full_name
        super().save_model(request, obj, form, change)


admin.site.register(UserProfile, UserProfileAdmin)

