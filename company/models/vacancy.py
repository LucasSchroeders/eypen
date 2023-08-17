from django.db import models

from users.choices import STATES, SENIORITY_CHOICES, JOB_MODALITY, JOB_TYPE


class Vacancy(models.Model):
    company = models.ForeignKey(
        "company.Company",
        related_name="vacancies",
        on_delete=models.CASCADE,
        verbose_name="Empresa",
    )
    job_position = models.CharField(max_length=80, db_index=True, verbose_name="Cargo")
    seniority = models.CharField(
        max_length=30,
        verbose_name="Senioridade",
        choices=SENIORITY_CHOICES,
    )
    job_modality = models.CharField(
        max_length=50,
        verbose_name="Modalidade",
        choices=JOB_MODALITY,
    )
    job_type = models.CharField(
        max_length=50,
        verbose_name="Tipo de trabalho",
        choices=JOB_TYPE,
    )
    state = models.CharField(max_length=200, blank=True, null=True, verbose_name="Estado", choices=STATES)
    city = models.CharField(max_length=200, blank=True, null=True, verbose_name="Cidade")
    description = models.CharField(max_length=2000, verbose_name='Descrição')

    class Meta:
        verbose_name = "Vaga"
        verbose_name_plural = "Vagas"
        indexes = [
            models.Index(fields=['job_position']),
        ]

    def __str__(self):
        return str(self.pk)
    
    def create_step(self):
        return
