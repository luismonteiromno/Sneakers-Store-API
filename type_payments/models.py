from django.db import models


class TypePayments(models.Model):
    payment = models.CharField('Pagamento')

    def __str__(self):
        return self.payment

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
