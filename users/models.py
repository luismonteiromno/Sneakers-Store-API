from django.db import models
from django.contrib.auth.models import AbstractUser
from sneakers.models import Brands, Sneakers

TYPE_USERS = (
    ('client', 'Cliente'),
    ('employee', 'Funcionário'),
    ('admin', 'Admin')
)


class UserProfile(AbstractUser):
    username = models.CharField('Nome de Usuário')
    first_name = models.CharField('Nome', max_length=100)
    last_name = models.CharField('Sobrenome', max_length=100)
    full_name = models.CharField('Nome completo', max_length=200, blank=True, null=True)
    street = models.CharField('Rua', default='')
    state = models.CharField('Estado', default='')
    number_house = models.CharField('Número da casa', default='')
    complement = models.CharField('Complemento', blank=True, null=True)
    city = models.CharField('Cidade', default='')
    cep = models.CharField('CEP', default=00000-000)
    cpf = models.CharField('CPF', unique=True, max_length=11)
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Telefone', help_text='Insira o telefone com o DDD na frente ex:(00) 90000-0000', default='', blank=True, null=True)
    type_user = models.CharField('Tipo do Usuário', choices=TYPE_USERS)
    favorite_brands = models.ManyToManyField(Brands, verbose_name='Marcas Favoritas', blank=True)
    favorite_sneakers = models.ManyToManyField(Sneakers, verbose_name='Tênis Favoritos', blank=True)
    shopping_cart = models.ManyToManyField(Sneakers, verbose_name='Carrinho de compras', related_name='user_shopping_cart', blank=True)
    notification_active = models.BooleanField('Notificações Ativas', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
