from django.db import models

from users.choices import VULNERABILITIES_CHOICES


class Step(models.Model):
    vacancy = models.ForeignKey(
        "company.Vacancy",
        related_name="steps",
        on_delete=models.CASCADE,
        verbose_name="Vagas",
    )
    step = models.IntegerField(    
        verbose_name="Número da etapa",
    )
    title = models.CharField(max_length=80, db_index=True, verbose_name="Nome da etapa")
    step_modality = models.CharField(max_length=50, verbose_name="Modalidade")
    step_type = models.CharField(max_length=80, verbose_name="Tipo da etapa")
    step_vulnerability = models.CharField(max_length=80, choices=VULNERABILITIES_CHOICES, verbose_name="Para quem é a etapa")
    description = models.CharField(max_length=2000, verbose_name='Descrição')

    class Meta:
        verbose_name = "Etapa"
        verbose_name_plural = "Etapas"
        indexes = [
            models.Index(fields=['title']),
        ]

    def __str__(self):
        return str(self.pk)
