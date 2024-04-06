from django.contrib import admin
from django.http import HttpRequest
from users.models import TYPE_USERS
from .models import AboutUs, TermsOfUse, PrivacyPolicy


class AboutUsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Sobre nós', {'fields': ('company', 'phone', 'description')}),
        ('Redes sociais', {'fields': ('facebook', 'instagram', 'whatsapp')})
    )

    def has_add_permission(self, request, obj=None):
        if request.user.type_user == 'admin':
            return True
    
    def has_change_permission(self, request, obj=None):
        if request.user.type_user == 'admin':
            return True
    
    def has_delete_permission(self, request, obj=None):
        if request.user.type_user == 'admin':
            return True
    
class TermsOfUseAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Termos de uso', {'fields': ('terms_of_use', 'terms_of_use_date')}),
    )
    
    def has_add_permission(self, request, obj=None):
        if request.user.type_user == 'admin':
            return True
    
    def has_change_permission(self, request, obj=None):
        if request.user.type_user == 'admin':
            return True
    
    def has_delete_permission(self, request, obj=None):
        if request.user.type_user == 'admin':
            return True
        
class PrivacyPolicyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Politica de Privacidade', {'fields': ('privacy_policy', 'privacy_policy_date')}),
    )
    
    def has_add_permission(self, request, obj=None):
        if request.user.type_user == 'admin':
            return True
    
    def has_change_permission(self, request, obj=None):
        if request.user.type_user == 'admin':
            return True
    
    def has_delete_permission(self, request, obj=None):
        if request.user.type_user == 'admin':
            return True

admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(TermsOfUse, TermsOfUseAdmin)
admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)

