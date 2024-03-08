from django.db import models


class AboutUs(models.Model):
    company = models.CharField('Compania')
    phone = models.CharField('Telefone')
    description = models.TextField('Sobre nós', max_length=300)
    facebook = models.URLField('Facebook', blank=True, null=True)
    instagram = models.URLField('Instagram', blank=True, null=True)
    whatsapp = models.URLField('Whatsapp', blank=True, null=True)

    def __str__(self):
        return f"{self.company} - {self.phone}"

    class Meta:
        verbose_name = 'Sobre nós'
        verbose_name_plural = 'Sobre nós'


class TermsOfUse(models.Model):
    terms = models.FileField('Termos de Uso', upload_to='terms_of_use/')

    def __str__(self):
        return str(self.terms)

    class Meta:
        verbose_name = 'Termo de Uso'
        verbose_name_plural = 'Termos de Uso'


class PrivacyPolicy(models.Model):
    privacy_policy = models.FileField('Politica de Privacidade', upload_to='privacy_police/')

    def __str__(self):
        return str(self.privacy_policy)

    class Meta:
        verbose_name = 'Politica de Privacidade'
        verbose_name_plural = 'Politicas de Privacidade'
