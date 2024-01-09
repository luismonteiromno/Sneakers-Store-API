from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email']


admin.site.register(UserProfile, UserProfileAdmin)

