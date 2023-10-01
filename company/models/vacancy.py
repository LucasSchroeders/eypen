from django.db import models

from company.models import Step
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
        blank=True,
    )
    candidates_step = models.ManyToManyField(
        'users.Profile',
        related_name='vacancies_step',
        verbose_name='Candidatos da etepa',
        blank=True,
    )
    approved_candidates = models.ManyToManyField(
        'users.Profile',
        related_name='vacancies_approved',
        verbose_name='Candidatos aprovados',
        blank=True,
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
            self.candidates_step.add(profile)
            return True
        return False

    def approve_candidates(self, list_candidates):
        for candidate in self.candidates_step.all():
            if str(candidate.id) in list_candidates:
                self.candidates_step.remove(candidate)

        candidates = list()
        for id_candidate in list_candidates:
            profile = Profile.objects.filter(id=id_candidate).first()
            self.approved_candidates.add(profile)
            candidates.append(profile.to_dict())
        return candidates

    def remove_approved_candidates(self, list_candidates):
        for candidate in self.approved_candidates.all():
            if str(candidate.id) in list_candidates:
                self.approved_candidates.remove(candidate)

        candidates = list()
        for id_candidate in list_candidates:
            profile = Profile.objects.filter(id=id_candidate).first()
            self.candidates_step.add(profile)
            candidates.append(profile.to_dict())
        return candidates

    def finish_step_selective_process(self):
        self.candidates_step.clear()
        # step = self.steps.filter(status='PEN').order_by('step').first()
        steps = self.steps.filter(status='PEN').order_by('step')
        exits_next_step = len(steps) > 1
        step = steps.first()
        step.status = 'ENC'
        step.save()

        if not exits_next_step:
            return

        for candidate in self.approved_candidates.all():
            self.candidates_step.add(candidate)
        
        self.approved_candidates.clear()
    def create_notification(self, message, is_all_candidates_step=True):
        if is_all_candidates_step:
            for candidate in self.candidates_step.all():
                notification = self.notification_vacancy.create(message=message)
                notification.profile = candidate
                notification.save()
        else:
            for candidate in self.approved_candidates.all():
                notification = self.notification_vacancy.create(message=message)
                notification.profile = candidate
                notification.save()
