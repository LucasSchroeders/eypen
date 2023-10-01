from django.db import models


class Notification(models.Model):
    message = models.CharField(max_length=250, verbose_name='Mensagem')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    profile = models.ForeignKey(
        'users.Profile',
        related_name='notification_profile',
        on_delete=models.CASCADE,
        verbose_name='Perfil',
    )
    vacancy = models.ForeignKey(
        'company.Vacancy',
        related_name='notification_vacancy',
        on_delete=models.CASCADE,
        verbose_name='Vaga',
    )

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"

    def __str__(self):
        return str(self.pk)
