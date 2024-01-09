from django.db import models
from django.contrib.auth.models import AbstractUser
from sneakers.models import Brands


class UserProfile(AbstractUser):
    username = models.CharField('Nome de Usuário')
    first_name = models.CharField('Nome', max_length=100)
    last_name = models.CharField('Sobrenome', max_length=100)
    full_name = models.CharField('Nome completo', max_length=200)
    cpf = models.CharField('CPF', unique=True, max_length=11)
    email = models.EmailField('Email', unique=True)
    favorite_brands = models.ManyToManyField(Brands, verbose_name='Marcas Favoritas', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
