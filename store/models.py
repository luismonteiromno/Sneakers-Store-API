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
    city = models.CharField('Cidade')
    cnpj = models.CharField('CNPJ', max_length=14, unique=True)
    email = models.EmailField('Email', unique=True)
    facebook = models.URLField('Facebook', blank=True, null=True)
    instagram = models.URLField('Instagram', blank=True, null=True)
    whatsapp = models.URLField('Whatsapp', blank=True, null=True)
    owner = models.ManyToManyField(UserProfile, verbose_name='Dono(s)', related_name='onwers_store')
    employees = models.ManyToManyField(UserProfile, verbose_name='Funcionários', related_name='store_employee')
    products = models.ManyToManyField(Sneakers, verbose_name='Tênis Disponiveis', related_name='sneakers_store')
    type_payments = models.ManyToManyField(TypePayments, verbose_name='Tipos de Pagamentos Aceitáveis', related_name='type_payments_store')
    opening_time = models.TimeField('Horário de abertura', default='08:00')
    closing_time = models.TimeField('Horário de fechamento', default='21:00')
    delivery = models.BooleanField('Faz entrega', default=False)
    minimum_delivery = models.IntegerField('Tempo minímo de entrega', default=0, blank=True, null=True)
    maximum_delivery = models.IntegerField('Tempo máximo de entrega', default=60, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Loja'
        verbose_name_plural = 'Lojas'
