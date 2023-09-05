from django.db import models

from users.choices import JOB_MODALITY, JOB_TYPE
from users.utils import string_to_date


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

    def to_dict(self):
        return {
            'id': self.pk,
            'position': self.position,
            'job_type': self.job_type,
            'job_modality': self.job_modality,
            'is_working': self.is_working,
            'company': self.company,
            'business_area': self.business_area,
            'started_at': self.started_at,
            'ended_at': self.ended_at,
        }
    
    def update(self, context):
        if context.get('position'):
            self.position = context.get('position')

        if context.get('job_type'):
            self.job_type = context.get('job_type')

        if context.get('job_modality'):
            self.job_modality = context.get('job_modality')
            
        if context.get('is_working'):
            self.is_working = context.get('is_working')

        if context.get('company'):
            self.company = context.get('company')

        if context.get('business_area'):
            self.business_area = context.get('business_area')

        if context.get('started_at'):
            started_at = string_to_date(context.get('started_at'))
            self.started_at = started_at

        if context.get('ended_at'):
            ended_at = string_to_date(context.get('ended_at'))
            self.ended_at = ended_at

        self.save()
        return self.to_dict()

    @property
    def get_url_photo(self):
        return "/static/images/experience.png"
