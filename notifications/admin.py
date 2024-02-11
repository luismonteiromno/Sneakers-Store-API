from django.contrib import admin
from .models import Notifications


class NotificationAdmin(admin.ModelAdmin):
    readonly_fields = ['send_date']
    list_display = ['email', 'subject', 'send_date']


admin.site.register(Notifications, NotificationAdmin)
