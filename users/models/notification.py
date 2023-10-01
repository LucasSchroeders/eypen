from django.db import models


class Notification(models.Model):
    message = models.CharField(max_length=250, verbose_name='Mensagem')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    profile = models.ForeignKey(
        'users.Profile',
        null=True,
        blank=True,
        related_name='notifications',
        on_delete=models.CASCADE,
        verbose_name='Perfil',
    )
    vacancy = models.ForeignKey(
        'company.Vacancy',
        related_name='notifications',
        on_delete=models.CASCADE,
        verbose_name='Vaga',
    )

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"

    def __str__(self):
        return str(self.pk)
