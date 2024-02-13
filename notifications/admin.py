from django.contrib import admin
from .models import Notifications


class NotificationAdmin(admin.ModelAdmin):
    readonly_fields = ['send_date']
    list_display = ['email', 'subject', 'send_date', 'is_read']
    list_filter = ['is_read']


admin.site.register(Notifications, NotificationAdmin)
