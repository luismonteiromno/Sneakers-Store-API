from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']
    filter_horizontal = ['favorite_brands', 'favorite_sneakers']
    list_filter = ['type_user']

    def save_model(self, request, obj, form, change):
        full_name = obj.first_name + ' ' + obj.last_name
        obj.full_name = full_name
        super().save_model(request, obj, form, change)


admin.site.register(UserProfile, UserProfileAdmin)

