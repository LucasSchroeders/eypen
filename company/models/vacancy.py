from django.db import models

from users.choices import (
    STATES,
    SENIORITY_CHOICES,
    JOB_MODALITY,
    JOB_TYPE,
    BUSINESS_AREAS_CHOICES,
    STATUS_VACANCY_CHOICES,
    VULNERABILITIES_CHOICES,
)
from users.models import Profile


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
    # TODO verificar se será mantido
    business_area = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        verbose_name="Areas de aplicação",
        choices=BUSINESS_AREAS_CHOICES,
    )
    status = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=STATUS_VACANCY_CHOICES,
        default='PEN',
        verbose_name='Status'
    )
    vulnerability = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Vulnerabilidade",
        choices=VULNERABILITIES_CHOICES,
    )
    state = models.CharField(max_length=200, blank=True, null=True, verbose_name="Estado", choices=STATES)
    city = models.CharField(max_length=200, blank=True, null=True, verbose_name="Cidade")
    description = models.CharField(max_length=2000, verbose_name='Descrição')
    candidates = models.ManyToManyField(
        'users.Profile',
        related_name='vacancies',
        verbose_name='Candidatos',
    )
    approved_candidates = models.ManyToManyField(
        'users.Profile',
        related_name='vacancies_approved',
        verbose_name='Candidatos aprovados',
    )

    class Meta:
        verbose_name = "Vaga"
        verbose_name_plural = "Vagas"
        indexes = [
            models.Index(fields=['job_position']),
        ]

    def __str__(self):
        return str(self.pk)
    
    def create_step(self, **context):
        step = self.steps.create(**context)
        
        return step.to_dict()
    
    def get_url_photo(self):
        return "/static/images/vaga.png"

    def register_candidate(self, id_profile):
        if not self.candidates.filter(id=id_profile).exists():
            profile = Profile.objects.filter(id=id_profile).first()
            self.candidates.add(profile)
            return True
        return False
