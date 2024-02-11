from django.db import models


class Notifications(models.Model):
    email = models.EmailField('Email')
    subject = models.CharField('Titulo')
    message = models.TextField('Mensagem', max_length=255)
    is_read = models.BooleanField('Foi lida', default=False)
    send_date = models.DateTimeField('Data de envio', auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.email} - {self.subject}"

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
