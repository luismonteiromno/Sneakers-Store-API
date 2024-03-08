from django.contrib import admin
from .models import AboutUs, TermsOfUse, PrivacyPolicy


class AboutUsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Sobre nós', {'fields': ('company', 'phone', 'description')}),
        ('Redes sociais', {'fields': ('facebook', 'instagram', 'whatsapp')})
    )


admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(TermsOfUse)
admin.site.register(PrivacyPolicy)
