from django.db import models


class AboutUs(models.Model):
    company = models.CharField('Compania')
    phone = models.CharField('Telefone')
    description = models.TextField('Sobre nós', max_length=300)

    def __str__(self):
        return f"{self.company} - {self.phone}"

    class Meta:
        verbose_name = 'Sobre nós'
        verbose_name_plural = 'Sobre nós'


class TermsOfUse(models.Model):
    terms = models.FileField(upload_to='terms_of_use/')

    def __str__(self):
        return str(self.terms)

    class Meta:
        verbose_name = 'Termo de Uso'
        verbose_name_plural = 'Termos de Uso'
