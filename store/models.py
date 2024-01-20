from django.db import models
from users.models import UserProfile
from sneakers.models import Sneakers
from type_payments.models import TypePayments
# Create your models here.


class Store(models.Model):
    name = models.CharField('Nome da Loja')
    street = models.CharField('Rua')
    number = models.CharField('Número')
    state = models.CharField('Estado')
    cnpj = models.CharField('CNPJ', max_length=14, unique=True)
    email = models.EmailField('Email', unique=True)
    facebook = models.URLField('Facebook', blank=True, null=True)
    instagram = models.URLField('Instagram', blank=True, null=True)
    whatsapp = models.URLField('Whatsapp', blank=True, null=True)
    owner = models.ManyToManyField(UserProfile, verbose_name='Dono(s)', related_name='onwers_store')
    products = models.ManyToManyField(Sneakers, verbose_name='Tênis Disponiveis', related_name='sneakers_store')
    type_payments = models.ManyToManyField(TypePayments, verbose_name='Tipos de Pagamentos Aceitáveis', related_name='type_payments_store')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Loja'
        verbose_name_plural = 'Lojas'
