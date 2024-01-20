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
    full_name = models.CharField('Nome completo', max_length=200)
    cpf = models.CharField('CPF', unique=True, max_length=11)
    email = models.EmailField('Email', unique=True)
    type_user = models.CharField('Tipo do Usuário', choices=TYPE_USERS)
    favorite_brands = models.ManyToManyField(Brands, verbose_name='Marcas Favoritas', blank=True)
    favorite_sneakers = models.ManyToManyField(Sneakers, verbose_name='Tênis Favoritos', blank=True)
    notification_active = models.BooleanField('Notificações Ativas', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
