from django.db import models

from users.choices import JOB_MODALITY, JOB_TYPE


class Experience(models.Model):
    profile = models.ForeignKey(
        'users.Profile',
        related_name='experience',
        on_delete=models.CASCADE,
        verbose_name='Perfil',
    )
    position = models.CharField(
        max_length=80,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="Cargo",
    )
    job_type = models.CharField(max_length=50, verbose_name='Tipo de trabalho', choices=JOB_TYPE)
    job_modality = models.CharField(max_length=50, verbose_name='Modalidade de trabalho', choices=JOB_MODALITY)
    is_working = models.BooleanField(default=False, verbose_name='Trabalhando atualmente')
    company = models.CharField(max_length=80, blank=True, null=True, verbose_name='Empresa')
    business_area = models.CharField(max_length=80, blank=True, null=True, verbose_name='Área de atuação da empresa')
    started_at = models.DateTimeField(verbose_name="Iniciado em")
    ended_at = models.DateTimeField(blank=True, null=True, verbose_name="Finalizado em")

    class Meta:
        verbose_name = 'Experiência'
        verbose_name_plural = 'Experiências'
        indexes = [
            models.Index(fields=['position']),
        ]

    def __str__(self):
        return str(self.pk)
