from django.db import models
from users.models import UserProfile
from sneakers.models import Sneakers


class Purchases(models.Model):
    sneaker = models.ManyToManyField(Sneakers, verbose_name='Tênis Comprado')
    user = models.ForeignKey(UserProfile, verbose_name='Usuário', related_name='user_purchase', on_delete=models.CASCADE)
    date_purchase = models.DateTimeField('Data da Compra', auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {str(self.date_purchase)}"

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
